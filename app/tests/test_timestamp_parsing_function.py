import unittest

from timestamp.timestamp_parsing_function import analyze_timestamp


class TestTimestampAnalysis(unittest.TestCase):
    """Unit tests for the timestamp analysis function."""

    def test_valid_iso_timestamps(self):
        """Test valid ISO 8601 formatted timestamps."""
        self.assertEqual(
            analyze_timestamp("2021-12-03T16:15:30.235Z"), "2021-12-03T16:15:30.235Z"
        )
        self.assertEqual(
            analyze_timestamp("2021-12-03T16:15:30.235"), "2021-12-03T16:15:30.235Z"
        )

    def test_unix_timestamps(self):
        """Test valid UNIX timestamps in seconds and milliseconds."""
        self.assertEqual(analyze_timestamp(1726667942), "2024-09-18T13:59:02.000Z")
        self.assertEqual(analyze_timestamp(969286895000), "2000-09-18T14:21:35.000Z")
        self.assertEqual(analyze_timestamp("1726668850124"), "2024-09-18T14:14:10.124Z")

    def test_edge_cases(self):
        """Test edge cases for timestamps at the SECONDS_THRESHOLD."""
        self.assertEqual(analyze_timestamp(10_000_000_000), "2286-11-20T17:46:40.000Z")
        self.assertEqual(
            analyze_timestamp(10_000_000_000_000), "2286-11-20T17:46:40.000Z"
        )

    def test_float_timestamps(self):
        """Test valid float timestamps for precision."""
        self.assertEqual(analyze_timestamp(1726667942.123), "2024-09-18T13:59:02.123Z")
        self.assertEqual(
            analyze_timestamp(969286895000.789), "2000-09-18T14:21:35.000Z"
        )

    def test_invalid_timestamps(self):
        """Test invalid timestamps to ensure proper error handling."""
        with self.assertRaises(ValueError):
            analyze_timestamp("invalid")

        with self.assertRaises(ValueError):
            analyze_timestamp(-1234567890)

        with self.assertRaises(ValueError):
            analyze_timestamp("abc123")


if __name__ == "__main__":
    unittest.main()
