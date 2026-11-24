#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news front page (1024x1024 PNG).

Self-authored build-time script for the make.fun news-image-20261124 entry.
Everything is drawn with PIL primitives: paper, rules, masthead, a cracked
globe illustration for the COP31 lead story, and four small drawn icons.
No downloaded images, no starter-kit assets.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 247, 237)   # warm newsprint
INK = (22, 21, 19)
RED = (179, 38, 30)
BLUE = (31, 78, 121)
OCEAN = (169, 198, 222)
OCEAN_DARK = (127, 168, 201)
LAND = (76, 122, 69)
GRAY = (107, 101, 92)
TINT = (239, 231, 214)    # icon tile background

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(f, s):
    return f.getlength(s)


def wrap(text, f, max_w):
    """Greedy word wrap, returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(f, trial) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_size(path, text, max_w, start):
    """Largest font size (<= start) whose text fits max_w."""
    size = start
    while size > 10 and text_w(font(path, size), text) > max_w:
        size -= 1
    return font(path, size)


def draw_tracked(d, cx, y, text, f, fill, tracking=0):
    """Draw text centred on cx at top y, with extra tracking between chars."""
    total = sum(f.getlength(ch) for ch in text) + tracking * max(len(text) - 1, 0)
    x = cx - total / 2
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += f.getlength(ch) + tracking
    return total


def draw_tracked_left(d, x, y, text, f, fill, tracking=0):
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += f.getlength(ch) + tracking


def draw_globe(d, cx, cy, r):
    """Stylised cracked globe: blue ocean, green land blobs, jagged crack."""
    # ocean
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=OCEAN, outline=INK, width=4)
    # meridians / parallels
    for k in (-0.55, 0, 0.55):
        d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                  outline=OCEAN_DARK, width=2) if k == 0 else None
    d.ellipse([cx - r, cy - r * 0.42, cx + r, cy + r * 0.42],
              outline=OCEAN_DARK, width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=OCEAN_DARK, width=2)
    # land blobs (abstract, deliberately not a real map)
    d.ellipse([cx - r * 0.78, cy - r * 0.72, cx - r * 0.08, cy - r * 0.12],
              fill=LAND)
    d.ellipse([cx + r * 0.05, cy + r * 0.05, cx + r * 0.72, cy + r * 0.62],
              fill=LAND)
    d.ellipse([cx + r * 0.28, cy - r * 0.55, cx + r * 0.8, cy - r * 0.05],
              fill=LAND)
    d.ellipse([cx - r * 0.55, cy + r * 0.35, cx - r * 0.05, cy + r * 0.8],
              fill=LAND)
    # jagged crack across the globe
    crack = [(cx - r * 0.95, cy - r * 0.55), (cx - r * 0.45, cy - r * 0.25),
             (cx - r * 0.55, cy + r * 0.05), (cx - r * 0.05, cy + r * 0.3),
             (cx - r * 0.2, cy + r * 0.6), (cx + r * 0.35, cy + r * 0.85)]
    d.line(crack, fill=PAPER, width=9, joint="curve")
    d.line(crack, fill=INK, width=4, joint="curve")
    # falling shards (kept inside the globe's block, above the divider)
    d.polygon([(cx + r * 0.55, cy + r * 0.92), (cx + r * 0.72, cy + r * 1.0),
               (cx + r * 0.5, cy + r * 1.04)], fill=RED)
    d.polygon([(cx - r * 0.1, cy + r * 0.96), (cx + r * 0.06, cy + r * 1.03),
               (cx - r * 0.13, cy + r * 1.06)], fill=INK)


def icon_ship(d, x, y, s):
    """Small ship + waves in a tinted tile."""
    d.rectangle([x, y, x + s, y + s], fill=TINT)
    # hull
    d.polygon([(x + 10, y + 38), (x + 54, y + 38), (x + 48, y + 50),
               (x + 16, y + 50)], fill=BLUE)
    # mast + flag
    d.line([(x + 32, y + 38), (x + 32, y + 14)], fill=INK, width=3)
    d.polygon([(x + 32, y + 14), (x + 48, y + 19), (x + 32, y + 24)],
              fill=RED)
    # waves
    d.line([(x + 8, y + 56), (x + 20, y + 52), (x + 32, y + 56),
            (x + 44, y + 52), (x + 56, y + 56)], fill=BLUE, width=3,
           joint="curve")


def icon_chip(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=TINT)
    # pins
    for i in (20, 32, 44):
        d.line([(x + i, y + 8), (x + i, y + 16)], fill=INK, width=3)
        d.line([(x + i, y + 48), (x + i, y + 56)], fill=INK, width=3)
        d.line([(x + 8, y + i), (x + 16, y + i)], fill=INK, width=3)
        d.line([(x + 48, y + i), (x + 56, y + i)], fill=INK, width=3)
    d.rectangle([x + 16, y + 16, x + 48, y + 48], fill=INK)
    d.rectangle([x + 24, y + 24, x + 40, y + 40], fill=RED)


def icon_scales(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=TINT)
    # post + beam
    d.line([(x + 32, y + 10), (x + 32, y + 52)], fill=INK, width=3)
    d.line([(x + 12, y + 18), (x + 52, y + 18)], fill=INK, width=3)
    d.line([(x + 22, y + 52), (x + 42, y + 52)], fill=INK, width=3)
    # pans
    for cxp in (14, 50):
        d.line([(x + cxp, y + 18), (x + cxp, y + 34)], fill=INK, width=2)
        d.polygon([(x + cxp - 9, y + 34), (x + cxp + 9, y + 34),
                   (x + cxp, y + 44)], fill=BLUE)


def icon_quake(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=TINT)
    # seismograph zigzag
    pts = [(x + 8, y + 32), (x + 18, y + 32), (x + 24, y + 18),
           (x + 30, y + 46), (x + 36, y + 24), (x + 42, y + 40),
           (x + 46, y + 32), (x + 56, y + 32)]
    d.line(pts, fill=RED, width=3, joint="curve")
    # ground crack
    d.line([(x + 10, y + 54), (x + 26, y + 50), (x + 40, y + 55),
            (x + 54, y + 51)], fill=INK, width=2, joint="curve")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    L, R = 48, 976
    CW = R - L

    # outer frame
    d.rectangle([20, 20, W - 20, H - 20], outline=INK, width=3)
    d.rectangle([28, 28, W - 28, H - 28], outline=INK, width=1)

    # ---- masthead ----
    mast = fit_size(SERIF_B, "THE DAILY WORLD", CW, 108)
    tw = text_w(mast, "THE DAILY WORLD")
    d.text(((W - tw) / 2, 46), "THE DAILY WORLD", font=mast, fill=INK)
    d.line([(L, 158), (R, 158)], fill=INK, width=2)

    # ---- date line (must read clearly) ----
    date_f = fit_size(SANS_B, "TUESDAY 24 NOVEMBER 2026", CW - 40, 40)
    draw_tracked(d, W / 2, 170, "TUESDAY 24 NOVEMBER 2026", date_f, INK, 4)
    d.line([(L, 220), (R, 220)], fill=INK, width=5)

    # ---- lead story: COP31 ----
    kick = font(SANS_B, 24)
    draw_tracked_left(d, L, 240, "CLIMATE SUMMIT  ·  ANTALYA", kick, RED, 3)
    head = fit_size(SANS_B, "COP31 COLLAPSES", CW, 104)
    d.text((L, 272), "COP31 COLLAPSES", font=head, fill=INK)

    sub_f = font(SANS, 27)
    sub = ("90+ nations reject the final draft after almost 50 hours of "
           "overtime talks — it never mentions fossil fuels.")
    sub_lines = wrap(sub, sub_f, 560)
    y = 396
    for ln in sub_lines:
        d.text((L, y), ln, font=sub_f, fill=INK)
        y += 36

    draw_globe(d, 812, 448, 92)

    # ---- divider ----
    d.line([(L, 556), (R, 556)], fill=INK, width=3)
    d.line([(L, 562), (R, 562)], fill=INK, width=1)

    # ---- also today ----
    also_f = font(SANS_B, 22)
    draw_tracked(d, W / 2, 576, "ALSO TODAY", also_f, INK, 6)
    d.line([(L, 586), (W / 2 - 130, 586)], fill=INK, width=1)
    d.line([(W / 2 + 130, 586), (R, 586)], fill=INK, width=1)

    # ---- 2x2 grid ----
    stories = [
        ("UKRAINE", "Sea drone sinks Russian warship",
         "Kyiv says its sea drone sank the corvette Merkury in Benghazi, Libya.",
         icon_ship),
        ("NVIDIA", "Huang returns as Nvidia CEO",
         "Huang is back after Trump intervened; the US blacklists Megaspeed too.",
         icon_chip),
        ("ROHINGYA", "14 nations back ICJ ruling",
         "Fourteen nations back the ICJ ruling on Myanmar's genocide of the Rohingya.",
         icon_scales),
        ("NEPAL", "Quake 5.6 hits Nepal",
         "A magnitude 5.6 quake strikes near the border with China.",
         icon_quake),
    ]
    cell_w, cell_h, gap = 452, 170, 24
    x0, y0 = L, 612
    for i, (kicker, headline, subline, icon) in enumerate(stories):
        cx = x0 + (i % 2) * (cell_w + gap)
        cy = y0 + (i // 2) * (cell_h + 16)
        icon(d, cx, cy + 4, 64)
        tx = cx + 80
        tw_ = cell_w - 80
        kf = font(SANS_B, 18)
        draw_tracked_left(d, tx, cy, kicker, kf, RED, 2)
        hf = font(SANS_B, 30)
        hl = wrap(headline, hf, tw_)
        yy = cy + 26
        for ln in hl[:2]:
            d.text((tx, yy), ln, font=hf, fill=INK)
            yy += 36
        sf = font(SANS, 20)
        sl = wrap(subline, sf, tw_)
        yy += 2
        for ln in sl[:2]:
            d.text((tx, yy), ln, font=sf, fill=INK)
            yy += 26

    # ---- footer ----
    foot = font(SANS, 16)
    ft = "THE DAILY WORLD  ·  TUESDAY 24 NOVEMBER 2026"
    draw_tracked(d, W / 2, 980, ft, foot, GRAY, 2)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
