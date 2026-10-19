"""Exercise quota projections and input boundaries without relying on wall time."""

import argparse
import unittest
from datetime import timedelta

from quota_forecast import forecast, percentage, positive_hours, timestamp


class QuotaForecastTests(unittest.TestCase):
    def setUp(self):
        self.now = timestamp("2026-10-19T12:00:00Z")

    def test_short_window_exhausts_before_reset(self):
        reset = self.now + timedelta(hours=3)
        self.assertEqual(
            forecast(reset, 40, 5, self.now),
            "2026-10-19T13:20:00+00:00 — 1.67 hours before reset",
        )

    def test_weekly_window_resets_before_exhaustion(self):
        reset = self.now + timedelta(days=3)
        self.assertIn("2026-10-25T12:00:00+00:00", forecast(reset, 60, 168, self.now))
        self.assertIn("resets before", forecast(reset, 60, 168, self.now))

    def test_exhaustion_at_reset(self):
        reset = self.now + timedelta(hours=2)
        self.assertIn("coincides", forecast(reset, 50, 4, self.now))

    def test_no_history_and_empty_quota(self):
        reset = self.now + timedelta(hours=2)
        self.assertIn("insufficient", forecast(reset, 100, 4, self.now))
        self.assertIn("insufficient", forecast(reset, 50, 2, self.now))
        self.assertEqual(forecast(reset, 0, 4, self.now), "already exhausted")

    def test_invalid_window(self):
        for delta in (-1, 0, 6):
            with self.subTest(delta=delta), self.assertRaises(ValueError):
                forecast(self.now + timedelta(hours=delta), 50, 5, self.now)

    def test_offset_conversion(self):
        self.assertEqual(timestamp("2026-10-19T15:00:00+03:00"), self.now)

    def test_invalid_inputs(self):
        for parser, values in (
            (timestamp, ("2026-10-19", "2026-10-19T12:00:00", "bad")),
            (percentage, ("-1", "101", "nan", "inf", "bad")),
            (positive_hours, ("0", "-1", "4.5", "bad")),
        ):
            for value in values:
                with self.subTest(value=value), self.assertRaises(argparse.ArgumentTypeError):
                    parser(value)


if __name__ == "__main__":
    unittest.main()
