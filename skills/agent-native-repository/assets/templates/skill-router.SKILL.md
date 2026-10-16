---
name: <domain>-guide
description: <When to use this skill, in one sentence a model can match against a task. Say which tasks do not need it.>
---

# <Domain> guide

Follow the user's request and the repository instructions first. This is
guidance, not permission to expand the task.

Before implementing, read the [inventory](<path>) of existing <components /
modules / patterns> and reuse them; add anything new to it in the same change.

Read [core guidance](<path>) and [accepted decisions](<path>). Load only the
topic guide that can change the current work:

- [<Topic A>](<path>): <when>
- [<Topic B>](<path>): <when>

For disputed details, retrieve a bounded passage instead of loading the corpus:

    <lookup command> '<query>' --source <ID>

Do not load <the full archive> for routine work. Keep user findings, automated
checks and agent judgments distinct. Record in the decisions log only real user
decisions and concluded tests, never your own preferences.
