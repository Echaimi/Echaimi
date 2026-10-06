"""Convert the profile photo into a monochrome, self-typing ASCII SVG."""
from pathlib import Path
from html import escape
from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "ChatGPT Image 20 sept. 2026, 16_21_01 (2).jpg"
OUTPUT = ROOT / "elyas-ascii.svg"
RAMP = " .`:-=+*cs#%@"
COLS, ROWS = 80, 38

def main() -> None:
    image = Image.open(SOURCE).convert("L")
    image = ImageOps.fit(image, (COLS, ROWS), method=Image.Resampling.LANCZOS)
    image = ImageEnhance.Contrast(image).enhance(1.75)
    rows = []
    pixels = list(image.getdata())
    for row in range(ROWS):
        values = pixels[row * COLS:(row + 1) * COLS]
        rows.append("".join(RAMP[value * (len(RAMP) - 1) // 255] for value in values))
    svg_rows = []
    for index, row in enumerate(rows):
        text = escape(row).replace(" ", "&#160;")
        y, delay = index * 10 + 48, index * 0.12
        svg_rows.append(f'''<g clip-path="url(#clip-{index})"><text x="14" y="{y}">{text}</text></g><clipPath id="clip-{index}"><rect x="0" y="{y - 12}" width="0" height="12"><animate attributeName="width" from="0" to="450" dur="0.7s" begin="{delay:.2f}s" fill="freeze"/></rect></clipPath>''')
    OUTPUT.write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="450" height="430" viewBox="0 0 450 430" role="img" aria-label="ASCII portrait of Elyas Chaimi"><rect width="450" height="430" rx="10" fill="#0d1117"/><text x="14" y="25" fill="#8b949e" font-family="monospace" font-size="10">elyas@github:~/profile$ cat portrait.txt</text><g fill="#c9d1d9" font-family="monospace" font-size="9" xml:space="preserve">{''.join(svg_rows)}</g></svg>''', encoding="utf-8")

if __name__ == "__main__":
    main()
