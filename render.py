#!/usr/bin/env python3
"""Render the 22 November 2026 world-news front page, 1024x1024 PNG.

Build-time tool for the make.fun news-image-20261122 entry. The entry itself
(main.py) only copies the rendered entry.png; this script is kept in the repo
so anyone can see how the image was made. Deterministic: no randomness, no
dates from the clock, no network.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 231)
INK = (20, 20, 20)
RED = (180, 35, 24)
NAVY = (29, 53, 87)
OCHRE = (176, 124, 22)
TEAL = (31, 94, 90)
GREY = (90, 86, 78)
LIGHT = (233, 226, 210)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, xy, text, fnt, max_w, fill=INK, leading=None, align="left"):
    x, y = xy
    lh = leading or int(fnt.size * 1.22)
    for line in wrap(draw, text, fnt, max_w):
        if align == "center":
            lx = x + (max_w - draw.textlength(line, font=fnt)) / 2
        else:
            lx = x
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += lh
    return y


def rule(draw, x, y, w, color=INK, width=2):
    draw.line([(x, y), (x + w, y)], fill=color, width=width)


def kicker(draw, x, y, text, color=RED, size=21):
    f = font(SANS_B, size)
    draw.text((x, y), text, font=f, fill=color)
    return f


def burst(draw, bx, by, r, color=(230, 140, 30)):
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        x2 = bx + r * math.cos(a)
        y2 = by + r * math.sin(a)
        draw.line([(bx, by), (x2, y2)], fill=color, width=5)
    draw.ellipse([bx - r // 2, by - r // 2, bx + r // 2, by + r // 2],
                 fill=color)


# ------------------------------------------------------------------ icons
def icon_globe(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(58, 110, 165),
                 outline=NAVY, width=4)
    # land blobs
    draw.ellipse([cx - r * 0.62, cy - r * 0.55, cx - r * 0.05, cy - r * 0.05],
                 fill=(74, 140, 74))
    draw.ellipse([cx + r * 0.05, cy + r * 0.05, cx + r * 0.62, cy + r * 0.55],
                 fill=(74, 140, 74))
    draw.ellipse([cx - r * 0.15, cy - r * 0.75, cx + r * 0.3, cy - r * 0.35],
                 fill=(74, 140, 74))
    # crack
    draw.line([(cx - r * 0.3, cy - r * 0.7), (cx - r * 0.05, cy - r * 0.25),
               (cx - r * 0.3, cy + r * 0.1), (cx, cy + r * 0.55)],
              fill=RED, width=5)
    # smoke puffs above
    for (sx, sy, sr) in [(cx - 52, cy - r - 18, 16),
                         (cx - 18, cy - r - 34, 20),
                         (cx + 22, cy - r - 20, 15)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(150, 146, 138))


def icon_warship(draw, x, y, w, h):
    # a corvette listing to starboard, bow up, stern going under;
    # kept inside the 150px icon box so it never touches the text
    for (sx, sy, sr) in [(x + 24, y + 58, 10), (x + 40, y + 46, 13),
                         (x + 56, y + 56, 9)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(150, 146, 138))
    # hull, bow high on the right, stern low on the left
    draw.polygon([(x + 14, y + 76), (x + 118, y + 46), (x + 130, y + 56),
                  (x + 30, y + 94)], fill=(70, 80, 92))
    # deck edge
    draw.line([(x + 14, y + 76), (x + 118, y + 46)], fill=(150, 156, 164),
              width=3)
    # superstructure and mast near the bow
    draw.rectangle([x + 88, y + 40, x + 106, y + 55], fill=(120, 126, 134))
    draw.line([(x + 97, y + 40), (x + 97, y + 28)], fill=INK, width=3)
    # gun turret and barrel at the bow
    draw.rectangle([x + 104, y + 40, x + 116, y + 50], fill=(120, 126, 134))
    draw.line([(x + 116, y + 44), (x + 130, y + 38)], fill=INK, width=4)
    # explosion burst at the bow waterline
    burst(draw, x + 132, y + 50, 22)
    # sea
    for i in range(3):
        yy = y + h - 22 + i * 9
        draw.arc([x, yy - 8, x + w, yy + 8], 0, 180, fill=NAVY, width=3)


def icon_city_drone(draw, x, y, w, h):
    # skyline (kept inside the 150px icon box so it never touches the text)
    base = y + h - 16
    buildings = [(0, 55), (28, 92), (56, 44), (84, 78), (112, 52)]
    for bx, bh in buildings:
        draw.rectangle([x + bx, base - bh, x + bx + 24, base], fill=NAVY)
    # windows
    for bx, bh in buildings:
        for wy in range(base - bh + 10, base - 8, 18):
            draw.rectangle([x + bx + 6, wy, x + bx + 11, wy + 7], fill=(240, 200, 90))
    # drone, top-left of the icon box
    dx, dy = x + 26, y + 12
    draw.ellipse([dx - 10, dy - 6, dx + 10, dy + 6], fill=INK)
    for sx in (-22, 22):
        draw.ellipse([dx + sx - 8, dy - 8, dx + sx + 8, dy + 8],
                     outline=INK, width=3)
        draw.line([(dx, dy), (dx + sx, dy)], fill=INK, width=3)
    # dashed path
    for i in range(6):
        yy = dy + 26 + i * 12
        draw.line([(dx - 4, yy), (dx + 4, yy)], fill=RED, width=3)


def icon_factory(draw, x, y, w, h):
    # industrial site: halls, chimney, smoke, and a fire burst on the roof
    base = y + h - 16
    draw.rectangle([x + 8, base - 52, x + 78, base], fill=TEAL)
    draw.rectangle([x + 82, base - 34, x + 128, base], fill=OCHRE)
    # chimney
    draw.rectangle([x + 112, y + 8, x + 128, base - 34], fill=NAVY)
    # roofline windows
    for wx in (20, 40, 60):
        draw.rectangle([x + wx, base - 40, x + wx + 10, base - 28],
                       fill=(240, 200, 90))
    # smoke puffs above the chimney
    for (sx, sy, sr) in [(x + 120, y - 2, 11), (x + 136, y - 14, 14),
                         (x + 152, y - 26, 10)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(150, 146, 138))
    # fire burst on the left hall roof
    burst(draw, x + 42, base - 56, 20)
    # ground line
    draw.line([(x, base), (x + w, base)], fill=INK, width=3)


def icon_mercury(draw, x, y, w, h):
    # cratered planet with a small probe on an orbit arc
    cx, cy, r = x + 68, y + 66, 56
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(196, 178, 150),
                 outline=NAVY, width=4)
    # craters
    for (crx, cry, crr) in [(cx - 24, cy - 18, 12), (cx + 18, cy + 6, 15),
                            (cx + 4, cy - 30, 8), (cx - 6, cy + 26, 10),
                            (cx + 30, cy - 22, 7)]:
        draw.ellipse([crx - crr, cry - crr, crx + crr, cry + crr],
                     fill=(158, 140, 114))
    # orbit arc
    draw.arc([x - 6, y - 6, x + 150, y + 150], 200, 330, fill=TEAL, width=3)
    # probe on the arc, top right
    px, py = x + 128, y + 18
    draw.rectangle([px - 8, py - 6, px + 8, py + 6], fill=NAVY)
    draw.rectangle([px - 26, py - 3, px - 10, py + 3], fill=OCHRE)
    draw.rectangle([px + 10, py - 3, px + 28, py + 3], fill=OCHRE)


# ------------------------------------------------------------------ page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 38  # margin
    CW = W - 2 * M  # content width

    # ---- masthead
    y = 30
    kicker(d, M, y, "SUNDAY  •  22 NOVEMBER 2026  •  WORLD NEWS IN ONE IMAGE")
    y += 30
    f_title = font(SERIF_B, 74)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, y), title, font=f_title, fill=INK)
    y += 92
    rule(d, M, y, CW, INK, 4)
    y += 6
    rule(d, M, y, CW, INK, 1)
    y += 14

    # ---- lead story: COP31 (full width)
    lead_y = y
    lead_h = 250
    d.rectangle([M, lead_y, W - M, lead_y + lead_h], fill=LIGHT,
                outline=INK, width=2)
    # illustration left
    icon_globe(d, M + 130, lead_y + 142, 72)
    # kicker + headline right
    tx = M + 268
    twd = W - M - 24 - tx
    kicker(d, tx, lead_y + 18, "CLIMATE  •  LEAD STORY", size=20)
    hy = draw_wrapped(d, (tx, lead_y + 48), "COP31 CLIMATE TALKS COLLAPSE",
                      font(SERIF_B, 46), twd, leading=52)
    draw_wrapped(d, (tx, hy + 6),
                 "The summit ends in Antalya with no deal after the EU rejects "
                 "a text that never mentions fossil fuels.",
                 font(SANS, 23), twd, leading=29)
    y = lead_y + lead_h + 18

    # ---- row 2: two half panels
    row_h = 200
    half = (CW - 16) // 2
    panels = [
        ("LIBYA", "WARSHIP HIT AT BENGHAZI",
         "Sea drone hits a Russian corvette at Benghazi; reports say it sank.",
         "warship"),
        ("UKRAINE", "14 MISSING NEAR KYIV",
         "Russian drone hits a five-storey block in Dymer; 14 are missing.",
         "city"),
    ]
    for i, (kick, head, dek, kind) in enumerate(panels):
        x = M + i * (half + 16)
        d.rectangle([x, y, x + half, y + row_h], fill=PAPER,
                    outline=INK, width=2)
        ix, iy = x + 14, y + 44
        if kind == "warship":
            icon_warship(d, ix, iy, 150, 120)
        else:
            icon_city_drone(d, ix, iy, 150, 120)
        tx2 = x + 178
        tw2 = x + half - 14 - tx2
        kicker(d, tx2, y + 14, kick, size=17)
        hy2 = draw_wrapped(d, (tx2, y + 40), head, font(SERIF_B, 27), tw2,
                           leading=31)
        draw_wrapped(d, (tx2, hy2 + 4), dek, font(SANS, 19), tw2, leading=24)
    y += row_h + 18

    # ---- row 3: two half panels
    panels = [
        ("GULF", "IRAN STRIKE HITS BAHRAIN",
         "Bahrain says an Iranian strike hit a civilian site, wounding two.",
         "factory"),
        ("SPACE", "PROBE REACHES MERCURY",
         "ESA confirms BepiColombo is in orbit around Mercury after eight years.",
         "mercury"),
    ]
    for i, (kick, head, dek, kind) in enumerate(panels):
        x = M + i * (half + 16)
        d.rectangle([x, y, x + half, y + row_h], fill=PAPER,
                    outline=INK, width=2)
        if kind == "factory":
            icon_factory(d, x + 14, y + 44, 150, 120)
        else:
            icon_mercury(d, x + 14, y + 44, 150, 120)
        tx2 = x + 178
        tw2 = x + half - 14 - tx2
        kicker(d, tx2, y + 14, kick, size=17)
        hy2 = draw_wrapped(d, (tx2, y + 40), head, font(SERIF_B, 27), tw2,
                           leading=31)
        draw_wrapped(d, (tx2, hy2 + 4), dek, font(SANS, 19), tw2, leading=24)
    y += row_h + 18

    # ---- also-today strip
    strip_y = y
    strip_h = 92
    d.rectangle([M, strip_y, W - M, strip_y + strip_h], fill=NAVY)
    draw_wrapped(d, (M + 16, strip_y + 12),
                 "ALSO TODAY:  Democrats win 258 House seats, biggest since 1992  •  "
                 "Russian cargo ship Sparta II ablaze in the Baltic  •  "
                 "Nigeria funeral boat capsizes, 24 killed  •  "
                 "France protests enter sixth weekend  •  "
                 "Brazil storm kills 3, injures 162",
                 font(SANS_B, 19), CW - 32, fill=(246, 241, 231), leading=25)
    y = strip_y + strip_h + 14

    # ---- footer
    rule(d, M, y, CW, INK, 1)
    f_foot = font(SANS, 17)
    foot = "22 NOVEMBER 2026  •  THE DAY’S WORLD NEWS, IN ONE IMAGE"
    fw = d.textlength(foot, font=f_foot)
    d.text(((W - fw) / 2, y + 8), foot, font=f_foot, fill=GREY)

    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = main()
    img.save(out, "PNG", optimize=True)
    print(out, img.size)
