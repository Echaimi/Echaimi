"""Fetch Echaimi's public GitHub contribution calendar without a token."""
import json
import re
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "contributions.json"

class ContributionParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = []
        self.days_by_id = {}
        self.current_tooltip_target = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "td" and "data-date" in attributes:
            day = {
                "date": attributes["data-date"],
                "level": int(attributes.get("data-level", 0)),
                "count": int(attributes.get("data-count", 0)),
            }
            self.days.append(day)
            if day_id := attributes.get("id"):
                self.days_by_id[day_id] = day
        elif tag == "tool-tip":
            self.current_tooltip_target = attributes.get("for")

    def handle_data(self, data):
        if self.current_tooltip_target not in self.days_by_id:
            return

        match = re.search(r"(No|[\d,]+) contributions? on ", data)
        if not match:
            return

        count = 0 if match.group(1) == "No" else int(match.group(1).replace(",", ""))
        self.days_by_id[self.current_tooltip_target]["count"] = count

    def handle_endtag(self, tag):
        if tag == "tool-tip":
            self.current_tooltip_target = None

def main() -> None:
    request = Request("https://github.com/users/Echaimi/contributions", headers={"User-Agent": "Echaimi-profile-readme"})
    with urlopen(request, timeout=30) as response:
        content = response.read().decode("utf-8")
    parser = ContributionParser()
    parser.feed(content)
    days = parser.days
    if not days:
        raise RuntimeError("GitHub returned no contribution-day cells")
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps({"username": "Echaimi", "generated_at": date.today().isoformat(), "total": sum(day["count"] for day in days), "days": days}, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()
