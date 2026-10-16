// Claude Code hook behind the "commit and push at the end of every turn" rule
// in AGENTS.md. After an edit it remembers which worktree the file is in; when
// a turn ends it stops Claude from finishing while one of those worktrees, or
// the session's own, has uncommitted or unpushed work on a feature branch.
// Changes made only through shell commands in another worktree are not seen
// here, which is why the rule itself stays in AGENTS.md.
import { execFileSync } from 'node:child_process'
import { appendFileSync, existsSync, mkdirSync, readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'

function git(cwd, ...args) {
  try {
    return execFileSync('git', args, {
      cwd,
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore'],
    }).trim()
  } catch {
    return null
  }
}

const worktreeOf = (directory) => git(directory, 'rev-parse', '--show-toplevel')
const commonDirOf = (directory) =>
  git(directory, 'rev-parse', '--path-format=absolute', '--git-common-dir')

function nearestDirectory(path) {
  let directory = dirname(path)
  while (!existsSync(directory) && directory !== dirname(directory)) {
    directory = dirname(directory)
  }
  return directory
}

/** The default branch: origin/HEAD when known, else main. Work on it is not gated. */
function defaultBranchOf(worktree) {
  const head = git(worktree, 'symbolic-ref', '--quiet', '--short', 'refs/remotes/origin/HEAD')
  return head ? head.replace(/^origin\//, '') : 'main'
}

/** What still has to be committed or pushed in a worktree, or null. */
function pending(worktree) {
  const branch = git(worktree, 'branch', '--show-current')
  if (!branch || branch === defaultBranchOf(worktree)) return null
  if (git(worktree, 'status', '--porcelain')) return `${worktree}: uncommitted changes`
  // Compared with the branch of the same name on origin, not @{upstream}: a
  // push without --set-upstream leaves no upstream although the work is there.
  const remote = `refs/remotes/origin/${branch}`
  if (!git(worktree, 'rev-parse', '--verify', '--quiet', remote)) {
    return `${worktree}: branch ${branch} has never been pushed`
  }
  const ahead = git(worktree, 'rev-list', '--count', `${remote}..HEAD`)
  return ahead && ahead !== '0' ? `${worktree}: ${ahead} unpushed commit(s)` : null
}

const input = JSON.parse(readFileSync(0, 'utf8'))
const commonDir = commonDirOf(input.cwd)
// One file per session, in Git's common directory so every worktree shares it.
const record = commonDir && join(commonDir, 'claude-touched', String(input.session_id))

if (record && input.hook_event_name === 'PostToolUse') {
  const file = input.tool_input?.file_path
  const worktree = file && worktreeOf(nearestDirectory(file))
  if (worktree && commonDirOf(worktree) === commonDir) {
    mkdirSync(dirname(record), { recursive: true })
    appendFileSync(record, `${worktree}\n`)
  }
}

// stop_hook_active means this hook already sent Claude back once this turn;
// letting it finish then keeps a failing push from looping forever.
if (record && input.hook_event_name === 'Stop' && !input.stop_hook_active) {
  const touched = existsSync(record) ? readFileSync(record, 'utf8').split('\n') : []
  const worktrees = new Set([worktreeOf(input.cwd), ...touched].filter(Boolean))
  const problems = [...worktrees].filter(existsSync).map(pending).filter(Boolean)
  if (problems.length > 0) {
    console.log(
      JSON.stringify({
        decision: 'block',
        reason: `AGENTS.md: commit and push at the end of every turn. Pending:\n${problems.join('\n')}\nCommit with a message describing the change and push the branch, then finish. Never commit to or push the default branch.`,
      }),
    )
  }
}
