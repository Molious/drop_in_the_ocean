#!/usr/bin/env python3
"""Generates the Night Shift Interactive logo SVGs.

The wordmark is drawn from custom monoline glyphs (no font dependency), so the
SVGs render identically everywhere. Run: python3 build.py
"""
import math
from pathlib import Path

OUT = Path(__file__).parent / "svg"

# Palette
BG = "#0B0820"
INK = "#F1EDFF"
PURPLE_DEEP = "#5B21D6"
PURPLE = "#9B5CFF"
AQUA = "#3FF2E3"
AQUA_DEEP = "#14B4D9"

# Monoline glyphs on a 100-unit cap height: (advance width, path data).
GLYPHS = {
    "N": (70, "M0,100 V0 L70,100 V0"),
    "I": (0, "M0,0 V100"),
    "G": (70, "M70,0 H30 A30,30 0 0 0 0,30 V70 A30,30 0 0 0 30,100 H70 V56 H42"),
    "H": (70, "M0,0 V100 M70,0 V100 M0,50 H70"),
    "T": (70, "M0,0 H70 M35,0 V100"),
    "S": (70, "M70,0 H25 A25,25 0 0 0 25,50 H45 A25,25 0 0 1 45,100 H0"),
    "F": (64, "M64,0 H0 V100 M0,50 H52"),
    "E": (64, "M64,0 H0 V100 H64 M0,50 H52"),
    "R": (70, "M0,100 V0 H45 A25,25 0 0 1 45,50 H0 M38,50 L70,100"),
    "A": (74, "M0,100 L37,0 L74,100 M17,54 H57"),
    "C": (70, "M70,0 H30 A30,30 0 0 0 0,30 V70 A30,30 0 0 0 30,100 H70"),
    "V": (74, "M0,0 L37,100 L74,0"),
}
SPACE = 46


def text_paths(text, tracking):
    """Returns (list of (x_offset, path)), total width in glyph units."""
    x, out = 0.0, []
    for i, ch in enumerate(text):
        if ch == " ":
            x += SPACE
            continue
        w, d = GLYPHS[ch]
        out.append((x, d))
        x += w + (tracking if i < len(text) - 1 else 0)
    return out, x


def text_group(text, tracking, x, y, scale, stroke, color, extra=""):
    parts, _ = text_paths(text, tracking)
    paths = "".join(
        f'<path transform="translate({px:g},0)" d="{d}"/>' for px, d in parts
    )
    return (
        f'<g transform="translate({x:g},{y:g}) scale({scale:g})" fill="none" '
        f'stroke="{color}" stroke-width="{stroke / scale:g}" stroke-linejoin="bevel" '
        f'stroke-linecap="butt"{extra}>{paths}</g>'
    )


def defs(uid):
    return f"""<defs>
  <linearGradient id="{uid}-aqua" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{AQUA}"/><stop offset="1" stop-color="{AQUA_DEEP}"/>
  </linearGradient>
  <linearGradient id="{uid}-ring" x1="0" y1="1" x2="1" y2="0">
    <stop offset="0" stop-color="{PURPLE_DEEP}"/><stop offset="1" stop-color="{PURPLE}"/>
  </linearGradient>
  <filter id="{uid}-glow-aqua" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur in="SourceGraphic" stdDeviation="14" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="{uid}-glow-purple" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur in="SourceGraphic" stdDeviation="9" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <mask id="{uid}-crescent">
    <circle cx="252" cy="264" r="134" fill="#fff"/>
    <circle cx="314" cy="216" r="116" fill="#000"/>
  </mask>
</defs>"""


def _ring_point(deg, cx=256, cy=256, r=200):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def badge(uid, mono=None):
    """Badge mark on a 512x512 canvas: broken ring, crescent, star.

    With `mono` set to a color, draws a flat single-color version (no
    gradients or glows) for print, embossing and one-color placements.
    """
    # Ring is an open arc with a gap at the upper right where the star sits.
    (x0, y0), (x1, y1) = _ring_point(-62), _ring_point(-22)
    ring = mono or f"url(#{uid}-ring)"
    moon = mono or f"url(#{uid}-aqua)"
    star = mono or INK
    glow_purple = "" if mono else f' filter="url(#{uid}-glow-purple)"'
    glow_aqua = "" if mono else f' filter="url(#{uid}-glow-aqua)"'
    return f"""<g>
  <path d="M {x0:.1f} {y0:.1f} A 200 200 0 1 0 {x1:.1f} {y1:.1f}" fill="none"
        stroke="{ring}" stroke-width="16" stroke-linecap="round"{glow_purple}/>
  <g{glow_aqua}>
    <rect x="0" y="0" width="512" height="512" fill="{moon}"
          mask="url(#{uid}-crescent)"/>
  </g>
  <path d="M396 92 L404 120 L432 128 L404 136 L396 164 L388 136 L360 128 L388 120 Z"
        fill="{star}"{glow_purple}/>
</g>"""


def svg(w, h, body, uid, bg=True, title=""):
    rect = f'<rect width="{w}" height="{h}" fill="{BG}"/>' if bg else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" role="img" aria-label="{title}">\n'
        f"<title>{title}</title>\n{defs(uid)}\n{rect}\n{body}\n</svg>\n"
    )


TITLE = "Night Shift Interactive"


def build_badge(bg, rounded=False, mono=None):
    uid = "nsb"
    body = badge(uid, mono)
    if rounded:
        # App-icon style tile: rounded square instead of full-bleed background.
        body = f'<rect x="0" y="0" width="512" height="512" rx="112" fill="{BG}"/>\n' + body
        return svg(512, 512, body, uid, bg=False, title=TITLE)
    return svg(512, 512, body, uid, bg=bg, title=TITLE)


def wordmark(x, top, mono=None):
    """Two-line wordmark. Returns (svg body, width, height)."""
    # Primary line: NIGHT SHIFT
    big_scale, big_track = 1.0, 26
    _, big_w = text_paths("NIGHT SHIFT", big_track)
    big_cap = 100 * big_scale
    # Secondary line: INTERACTIVE, tracked out to match the primary width.
    small_scale = 0.34
    raw = "INTERACTIVE"
    _, w0 = text_paths(raw, 0)
    small_track = (big_w * big_scale / small_scale - w0) / (len(raw) - 1)
    small_cap = 100 * small_scale

    gap = 34
    word = text_group("NIGHT SHIFT", big_track, x, top, big_scale, 15, mono or INK)
    sub = text_group(
        raw, small_track, x, top + big_cap + gap, small_scale, 6, mono or AQUA
    )
    return f"{word}\n{sub}", big_w * big_scale, big_cap + gap + small_cap


def build_lockup(bg, mono=None):
    uid = "nsl"
    H = 480
    badge_size = 360
    pad = (H - badge_size) / 2
    s = badge_size / 512
    mark = f'<g transform="translate({pad:g},{pad:g}) scale({s:g})">{badge(uid, mono)}</g>'

    text_x = pad + badge_size + 70
    _, _, block_h = wordmark(0, 0)
    words, text_w, _ = wordmark(text_x, (H - block_h) / 2, mono)
    total_w = text_x + text_w + pad
    return svg(round(total_w), H, f"{mark}\n{words}", uid, bg=bg, title=TITLE)


def build_stacked(bg, mono=None):
    uid = "nss"
    pad = 90
    badge_size = 400
    gap = 40
    _, text_w, block_h = wordmark(0, 0)
    W = text_w + 2 * pad
    s = badge_size / 512
    bx = (W - badge_size) / 2
    mark = f'<g transform="translate({bx:g},{pad:g}) scale({s:g})">{badge(uid, mono)}</g>'
    words, _, _ = wordmark(pad, pad + badge_size + gap, mono)
    H = pad + badge_size + gap + block_h + pad
    return svg(round(W), round(H), f"{mark}\n{words}", uid, bg=bg, title=TITLE)


def main():
    (OUT / "mono").mkdir(parents=True, exist_ok=True)
    files = {
        "nsi-lockup-dark.svg": build_lockup(bg=True),
        "nsi-lockup-transparent.svg": build_lockup(bg=False),
        "nsi-stacked-dark.svg": build_stacked(bg=True),
        "nsi-stacked-transparent.svg": build_stacked(bg=False),
        "nsi-badge-dark.svg": build_badge(bg=True),
        "nsi-badge-transparent.svg": build_badge(bg=False),
        "nsi-badge-app-icon.svg": build_badge(bg=False, rounded=True),
    }
    # Monochrome variants on transparent backgrounds: white for dark
    # surfaces, black for light surfaces.
    for tone, color in (("white", "#FFFFFF"), ("black", "#000000")):
        files[f"mono/nsi-lockup-mono-{tone}.svg"] = build_lockup(bg=False, mono=color)
        files[f"mono/nsi-stacked-mono-{tone}.svg"] = build_stacked(bg=False, mono=color)
        files[f"mono/nsi-badge-mono-{tone}.svg"] = build_badge(bg=False, mono=color)
    for name, content in files.items():
        (OUT / name).write_text(content)
        print("wrote", OUT / name)


if __name__ == "__main__":
    main()
