"""Render a transparent GitHub-style contribution calendar SVG."""
import json
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GITHUB_PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
CELL_SIZE = 12
CELL_GAP = 3
GRID_X = 50
GRID_Y = 55


def calendar_layout(days):
    """Return GitHub-calendar positions as (date, level, week, weekday)."""
    calendar_start = min(date.fromisoformat(entry["date"]) for entry in days)
    calendar_start -= timedelta(days=(calendar_start.weekday() + 1) % 7)
    positions = []
    for entry in sorted(days, key=lambda item: item["date"]):
        current = date.fromisoformat(entry["date"])
        week, weekday = divmod((current - calendar_start).days, 7)
        positions.append((entry["date"], entry["level"], week, weekday))
    return positions


def main() -> None:
    payload = json.loads((ROOT / "data" / "contributions.json").read_text(encoding="utf-8"))
    layout = calendar_layout(payload["days"])
    first_day = date.fromisoformat(layout[0][0])
    month_labels = []
    for value, _, week, _ in layout:
        current = date.fromisoformat(value)
        if current == first_day or current.day == 1:
            x = GRID_X + week * (CELL_SIZE + CELL_GAP)
            month_labels.append(
                f'<text x="{x}" y="43" fill="#8b949e" '
                f'font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" '
                f'font-size="10">{current:%b}</text>'
            )
    cells = []
    for _, level, week, weekday in layout:
        x = GRID_X + week * (CELL_SIZE + CELL_GAP)
        y = GRID_Y + weekday * (CELL_SIZE + CELL_GAP)
        color = GITHUB_PALETTE[min(level, len(GITHUB_PALETTE) - 1)]
        delay = 0.15 + (week + weekday) * 0.045
        cells.append(
            f'<g opacity="0"><rect x="{x}" y="{y}" width="{CELL_SIZE}" height="{CELL_SIZE}" rx="2" fill="{color}"/>'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.25s" begin="{delay:.3f}s" fill="freeze"/></g>'
        )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="165" viewBox="0 0 860 165" role="img" aria-label="{payload['total']} contributions in the last year">
<text x="20" y="21" fill="#c9d1d9" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="13">{payload['total']:,} contributions in the last year</text>
{''.join(month_labels)}
<g>{''.join(cells)}</g>
<g fill="#8b949e" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif" font-size="10"><text x="12" y="79">Mon</text><text x="12" y="109">Wed</text><text x="12" y="139">Fri</text></g>
</svg>'''
    (ROOT / "contrib-heatmap.svg").write_text(svg, encoding="utf-8")
    return
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="215" viewBox="0 0 860 215" role="img" aria-label="{payload['total']} contributions in the last year">
<rect width="860" height="215" rx="10" fill="#0b1220"/>
<rect x="1" y="1" width="858" height="213" rx="9" fill="none" stroke="#1f6f43"/>
<rect x="20" y="19" width="4" height="20" rx="2" fill="#39d353"/>
<circle cx="842" cy="29" r="4" fill="#39d353"><animate attributeName="opacity" values="1;0.35;1" dur="1.8s" repeatCount="indefinite"/></circle>
<text x="32" y="29" fill="#a7f3d0" font-family="monospace" font-size="10" letter-spacing="1">CONTRIBUTION ACTIVITY</text>
<text x="32" y="47" fill="#e6ffef" font-family="monospace" font-size="15">Echaimi — {payload['total']:,} contributions in the last year</text>
<g>{''.join(cells)}</g>
<text x="26" y="76" fill="#7eaa8c" font-family="monospace" font-size="10">Sun</text><text x="26" y="104" fill="#7eaa8c" font-family="monospace" font-size="10">Tue</text><text x="26" y="132" fill="#7eaa8c" font-family="monospace" font-size="10">Thu</text>
<text x="693" y="185" fill="#7eaa8c" font-family="monospace" font-size="10">Less</text>{legend}<text x="815" y="185" fill="#7eaa8c" font-family="monospace" font-size="10">More</text>
</svg>'''
    (ROOT / "contrib-heatmap.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
