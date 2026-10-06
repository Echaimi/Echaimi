import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("fetch_contributions.py")
SPEC = importlib.util.spec_from_file_location("fetch_contributions", MODULE_PATH)
fetch_contributions = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(fetch_contributions)


class ContributionParserTests(unittest.TestCase):
    def test_reads_counts_from_github_tooltips(self):
        parser = fetch_contributions.ContributionParser()
        parser.feed(
            '''
            <td data-date="2026-09-01" id="contribution-day-component-0-0" data-level="2"></td>
            <tool-tip for="contribution-day-component-0-0">3 contributions on September 1st.</tool-tip>
            <td data-date="2026-09-02" id="contribution-day-component-0-1" data-level="0"></td>
            <tool-tip for="contribution-day-component-0-1">No contributions on September 2nd.</tool-tip>
            '''
        )

        self.assertEqual(
            parser.days,
            [
                {"date": "2026-09-01", "level": 2, "count": 3},
                {"date": "2026-09-02", "level": 0, "count": 0},
            ],
        )


if __name__ == "__main__":
    unittest.main()
