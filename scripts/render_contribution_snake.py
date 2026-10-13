"""Render a standalone animated snake over the recorded contribution calendar."""

import json
from datetime import date, timedelta
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
PALETTE = ('#1E1B2E', '#312E81', '#5B21B6', '#8B5CF6', '#C4B5FD')


def render(payload):
    days = {date.fromisoformat(entry['date']): entry for entry in payload['days']}
    start = min(days)
    start -= timedelta(days=(start.weekday() + 1) % 7)
    weeks = (max(days) - start).days // 7 + 1
    width = 56 + weeks * 16
    cells, points = [], []
    for week in range(weeks):
        for weekday in range(7):
            current = start + timedelta(days=week * 7 + weekday)
            entry = days.get(current)
            if entry is None:
                continue
            x, y = 28 + week * 16, 48 + weekday * 16
            level = max(0, min(int(entry['level']), 4))
            count = int(entry['count'])
            cells.append(f'<rect x="{x}" y="{y}" width="12" height="12" rx="3" fill="{PALETTE[level]}"><title>{current}: {count} contributions</title></rect>')
        rows = range(7) if week % 2 == 0 else range(6, -1, -1)
        points.extend((34 + week * 16, 54 + row * 16) for row in rows)
    points.append(points[0])
    path = 'M ' + ' L '.join(f'{x},{y}' for x, y in points)
    duration = max(24, weeks * 0.7)
    segments = []
    for index in range(7, -1, -1):
        radius = 5.5 if index == 0 else 4.8 - index * 0.28
        color = '#EDE9FE' if index == 0 else '#A78BFA'
        delay = -(duration - index * duration / len(points))
        segments.append(f'<circle r="{radius:.2f}" fill="{color}" opacity="{1 - index * 0.075:.3f}"><animateMotion dur="{duration:.2f}s" begin="{delay:.3f}s" repeatCount="indefinite" calcMode="paced" path="{path}"/></circle>')
    username = escape(str(payload['username']))
    generated_at = escape(str(payload['generated_at']))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="196" viewBox="0 0 {width} 196" role="img" aria-labelledby="title description">
<title id="title">{username} contribution snake</title>
<desc id="description">Animated violet snake over recorded GitHub contributions. Snapshot: {generated_at}. {int(payload['total'])} contributions.</desc>
<rect width="{width}" height="196" rx="12" fill="#0D1117"/>
<rect x="0.5" y="0.5" width="{width - 1}" height="195" rx="12" fill="none" stroke="#312E81"/>
<text x="28" y="28" fill="#A78BFA" font-family="ui-monospace,monospace" font-size="11" letter-spacing="1.8">CONTRIBUTION SNAKE</text>
{''.join(cells)}
{''.join(segments)}
<text x="28" y="179" fill="#8B949E" font-family="ui-monospace,monospace" font-size="10">{int(payload['total'])} contributions / {generated_at}</text>
</svg>'''


def main():
    payload = json.loads((ROOT / 'data/contributions.json').read_text(encoding='utf-8'))
    (ROOT / 'contribution-snake.svg').write_text(render(payload), encoding='utf-8')


if __name__ == '__main__':
    main()
