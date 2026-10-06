"""Render contribution data as a one-shot animated SVG."""
import json
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def main() -> None:
    payload = json.loads((ROOT / "data" / "contributions.json").read_text(encoding="utf-8"))
    levels = {entry["date"]: entry["level"] for entry in payload["days"]}
    end = date.today()
    start = end - timedelta(days=370 + (end.weekday() + 1) % 7)
    cells = []
    for offset in range(371):
        current = start + timedelta(days=offset)
        week, weekday = divmod(offset, 7)
        x, y = 54 + week * 14, 65 + weekday * 14
        delay = 0.30 + (week + weekday) * 0.100
        cells.append(f'<rect x="{x}" y="{y}" width="10" height="10" rx="2" fill="{PALETTE[min(levels.get(current.isoformat(), 0), 5)]}" opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.60s" begin="{delay:.3f}s" fill="freeze"/></rect>')
    legend = "".join(f'<rect x="{730 + i * 13}" y="176" width="10" height="10" rx="2" fill="{color}"/>' for i, color in enumerate(PALETTE))
    (ROOT / "contrib-heatmap.svg").write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="215" viewBox="0 0 860 215" role="img" aria-label="{payload['total']} contributions in the last year"><rect width="860" height="215" rx="10" fill="#0d1117"/><rect x="1" y="1" width="858" height="213" rx="9" fill="none" stroke="#30363d"/><text x="26" y="35" fill="#c9d1d9" font-family="monospace" font-size="15">Echaimi — {payload['total']:,} contributions in the last year</text><g>{''.join(cells)}</g><text x="26" y="76" fill="#8b949e" font-family="monospace" font-size="10">Sun</text><text x="26" y="104" fill="#8b949e" font-family="monospace" font-size="10">Tue</text><text x="26" y="132" fill="#8b949e" font-family="monospace" font-size="10">Thu</text><text x="693" y="185" fill="#8b949e" font-family="monospace" font-size="10">Less</text>{legend}<text x="815" y="185" fill="#8b949e" font-family="monospace" font-size="10">More</text></svg>''', encoding="utf-8")

if __name__ == "__main__":
    main()
