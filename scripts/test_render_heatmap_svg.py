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

    def test_calendar_grid_uses_the_available_width(self):
        right_edge = (
            render_heatmap_svg.GRID_X
            + 52 * (render_heatmap_svg.CELL_SIZE + render_heatmap_svg.CELL_GAP)
            + render_heatmap_svg.CELL_SIZE
        )

        self.assertGreaterEqual(right_edge, 850)
class HeatmapSvgTests(unittest.TestCase):
    def test_renders_a_transparent_github_style_calendar(self):
        render_heatmap_svg.main()
        svg = (MODULE_PATH.parents[1] / "contrib-heatmap.svg").read_text(encoding="utf-8")

        self.assertNotIn("#0b1220", svg)
        self.assertNotIn("CONTRIBUTION ACTIVITY", svg)
        self.assertNotIn(">Less<", svg)
        self.assertNotIn(">More<", svg)
        self.assertIn("contributions in the last year", svg)
        self.assertIn('<text x="20" y="184"', svg)
        self.assertIn('attributeName="opacity"', svg)
        self.assertIn('opacity="0"', svg)
        self.assertIn('attributeName="transform" type="scale"', svg)
        self.assertIn('width="14"', svg)
        for color in ("#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"):
            self.assertIn(color, svg)


if __name__ == "__main__":
    unittest.main()
