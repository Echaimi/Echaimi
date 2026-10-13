"""Render a violet weekly activity graph from recorded GitHub contributions."""

import json
from datetime import date, timedelta
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]


def render(payload):
    days = payload['days']
    start = min(date.fromisoformat(day['date']) for day in days)
    start -= timedelta(days=start.weekday())
    end = max(date.fromisoformat(day['date']) for day in days)
    weeks = [0] * ((end - start).days // 7 + 1)
    for day in days:
        weeks[(date.fromisoformat(day['date']) - start).days // 7] += int(day['count'])
    peak = max(1, max(weeks))
    coordinates = [(54 + index * 752 / max(1, len(weeks) - 1), 226 - count * 148 / peak) for index, count in enumerate(weeks)]
    points = ' '.join(f'{x:.2f},{y:.2f}' for x, y in coordinates)
    ticks = []
    for step in range(5):
        y = 226 - step * 37
        ticks.append(f'<path d="M54 {y}H806" stroke="#24213A"/><text x="40" y="{y + 4}" fill="#8B949E" font-size="10" text-anchor="end">{peak * step / 4:.0f}</text>')
    dots = ''.join(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2.6" fill="#C4B5FD"><title>Week {index + 1}: {weeks[index]} contributions</title></circle>' for index, (x, y) in enumerate(coordinates))
    caption = escape(f"Weekly contributions / snapshot {payload['generated_at']}")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="282" viewBox="0 0 860 282" role="img" aria-labelledby="title description">
<title id="title">Elyas Chaimi contribution activity</title>
<desc id="description">{caption}. {int(payload['total'])} recorded contributions.</desc>
<defs><linearGradient id="area" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7C3AED" stop-opacity="0.4"/><stop offset="1" stop-color="#7C3AED" stop-opacity="0.02"/></linearGradient></defs>
<rect width="860" height="282" rx="12" fill="#0D1117"/>
<rect x="0.5" y="0.5" width="859" height="281" rx="12" fill="none" stroke="#312E81"/>
<g font-family="ui-monospace,monospace"><text x="28" y="31" fill="#A78BFA" font-size="14">CONTRIBUTION ACTIVITY</text>
<text x="28" y="51" fill="#8B949E" font-size="10">{caption}</text>
{''.join(ticks)}
<polygon points="54,226 {points} {coordinates[-1][0]:.2f},226" fill="url(#area)"/>
<polyline points="{points}" fill="none" stroke="#818CF8" stroke-width="2" stroke-linejoin="round"/>
{dots}
<text x="54" y="251" fill="#8B949E" font-size="10">{start.isoformat()}</text>
<text x="806" y="251" fill="#8B949E" font-size="10" text-anchor="end">{end.isoformat()}</text></g>
</svg>'''


def main():
    payload = json.loads((ROOT / 'data/contributions.json').read_text(encoding='utf-8'))
    (ROOT / 'contribution-activity.svg').write_text(render(payload), encoding='utf-8')


if __name__ == '__main__':
    main()
