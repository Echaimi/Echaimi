import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("render_heatmap_svg.py")
SPEC = importlib.util.spec_from_file_location("render_heatmap_svg", MODULE_PATH)
render_heatmap_svg = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(render_heatmap_svg)


class CalendarLayoutTests(unittest.TestCase):
    def test_uses_githubs_sunday_based_calendar(self):
        positions = render_heatmap_svg.calendar_layout(
            [
                {"date": "2025-10-05", "level": 1},  # Sunday
                {"date": "2025-10-06", "level": 2},  # Monday
                {"date": "2025-10-12", "level": 3},  # Following Sunday
            ]
        )

        self.assertEqual(
            positions,
            [
                ("2025-10-05", 1, 0, 0),
                ("2025-10-06", 2, 0, 1),
                ("2025-10-12", 3, 1, 0),
            ],
        )


if __name__ == "__main__":
    unittest.main()
