"""Render contribution data as a polished, animated SVG."""
import json
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PALETTE = ["#17251d", "#075c32", "#0b873f", "#16a34a", "#39d353", "#a7f3d0"]


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
    cells = []
    for _, level, week, weekday in calendar_layout(payload["days"]):
        x, y = 54 + week * 14, 65 + weekday * 14
        delay = 0.20 + (week + weekday) * 0.075
        color = PALETTE[min(level, 5)]
        cells.append(
            f'<rect x="{x + 5}" y="{y + 5}" width="0" height="0" rx="2" fill="{color}" opacity="0">'
            f'<animate attributeName="x" from="{x + 5}" to="{x}" dur="0.40s" begin="{delay:.3f}s" fill="freeze"/>'
            f'<animate attributeName="y" from="{y + 5}" to="{y}" dur="0.40s" begin="{delay:.3f}s" fill="freeze"/>'
            f'<animate attributeName="width" from="0" to="10" dur="0.40s" begin="{delay:.3f}s" fill="freeze"/>'
            f'<animate attributeName="height" from="0" to="10" dur="0.40s" begin="{delay:.3f}s" fill="freeze"/>'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.30s" begin="{delay:.3f}s" fill="freeze"/></rect>'
        )
    legend = "".join(
        f'<rect x="{730 + index * 13}" y="176" width="10" height="10" rx="2" fill="{color}"/>'
        for index, color in enumerate(PALETTE)
    )
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
