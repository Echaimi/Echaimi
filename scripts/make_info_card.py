"""Generate an animated terminal/neofetch profile card."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "info-card.svg"
ROWS = [("name", "Elyas Chaimi"), ("role", "Full Stack Developer"), ("location", "Paris, France"), ("focus", "RAG-powered AI applications"), ("stack", "TypeScript · React · Node.js"), ("backend", "FastAPI · NestJS · PostgreSQL"), ("ai", "LangChain · LlamaIndex · Hybrid search"), ("now", "Building useful, grounded LLM apps"), ("contact", "elyaschaimi@gmail.com")]

def main() -> None:
    rows = []
    for index, (key, value) in enumerate(ROWS):
        y, delay = 95 + index * 32, 0.5 + index * 0.35
        rows.append(f'''<g opacity="0" transform="translate(-8,0)"><text x="26" y="{y}" fill="#58a6ff">{escape(key).ljust(11)}</text><text x="145" y="{y}" fill="#c9d1d9">{escape(value)}</text><animate attributeName="opacity" from="0" to="1" dur="0.45s" begin="{delay:.2f}s" fill="freeze"/><animateTransform attributeName="transform" type="translate" from="-8 0" to="0 0" dur="0.45s" begin="{delay:.2f}s" fill="freeze"/></g>''')
    OUTPUT.write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="490" height="510" viewBox="0 0 490 510" role="img" aria-label="Elyas Chaimi terminal profile"><rect width="490" height="510" rx="10" fill="#0d1117"/><rect x="1" y="1" width="488" height="508" rx="9" fill="none" stroke="#30363d"/><circle cx="25" cy="25" r="6" fill="#ff5f57"/><circle cx="45" cy="25" r="6" fill="#febc2e"/><circle cx="65" cy="25" r="6" fill="#28c840"/><text x="92" y="29" fill="#8b949e" font-family="monospace" font-size="12">elyas@github — neofetch</text><line x1="20" y1="52" x2="470" y2="52" stroke="#30363d"/><text x="26" y="73" fill="#3fb950" font-family="monospace" font-size="13">● online</text><g font-family="monospace" font-size="12">{''.join(rows)}</g><text x="26" y="475" fill="#8b949e" font-family="monospace" font-size="11">$ _</text></svg>''', encoding="utf-8")

if __name__ == "__main__":
    main()
