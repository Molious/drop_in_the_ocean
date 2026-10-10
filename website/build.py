#!/usr/bin/env python3
"""Builds website/index.html from src/page.html, inlining the logo SVGs.

Run after changing the page or regenerating the logos: python3 build.py
"""
import re
from pathlib import Path

HERE = Path(__file__).parent
LOGOS = HERE.parent / "branding" / "night-shift-interactive" / "svg"

# Placeholder contact address. Replace with the studio's real inbox.
EMAIL = "hello@nightshiftinteractive.com"


def inline_svg(path, decorative=False, id_prefix=None):
    svg = path.read_text()
    # Size is set in CSS, so drop the fixed pixel dimensions and the <title>.
    svg = re.sub(r'\s(width|height)="\d+"', "", svg, count=2)
    svg = re.sub(r"<title>.*?</title>\n?", "", svg)
    if decorative:
        svg = svg.replace('role="img" aria-label="Night Shift Interactive"', 'aria-hidden="true"')
    if id_prefix:
        old = re.search(r'id="(\w+)-', svg).group(1)
        svg = svg.replace(f"{old}-", f"{id_prefix}-")
    return svg.strip()


def main():
    page = (HERE / "src" / "page.html").read_text()
    page = (
        page.replace("{{STACKED}}", inline_svg(LOGOS / "nsi-stacked-transparent.svg"))
        .replace("{{BADGE}}", inline_svg(LOGOS / "nsi-badge-transparent.svg", decorative=True))
        .replace("{{BADGE_MONO}}", inline_svg(LOGOS / "mono" / "nsi-badge-mono-white.svg", decorative=True, id_prefix="nsm"))
        .replace("{{EMAIL}}", EMAIL)
    )
    head, body = page.split('<header class="bar">', 1)
    html = (
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        f'{head}</head>\n<body>\n<header class="bar">{body}</body>\n</html>\n'
    )
    (HERE / "index.html").write_text(html)
    print("wrote", HERE / "index.html")


if __name__ == "__main__":
    main()
