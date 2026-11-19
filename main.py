#!/usr/bin/env python3
"""News poster for Thursday 19 November 2026.

Draws a one-page newspaper front page with PIL primitives only: a masthead
naming the day, a Vice City sunset hero for the GTA VI launch, six story
blocks across regions and beats, and a footer ticker. No network, no clock,
no randomness: two runs write byte-identical PNGs.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

PAPER = (247, 243, 232)
INK = (24, 22, 26)
NAVY = (18, 28, 54)
NAVY_DARK = (12, 19, 38)
GOLD = (201, 154, 52)
GOLD_PALE = (240, 205, 120)
CREAM = (247, 243, 232)
RULE = (120, 110, 92)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def sunset_sky(draw, x0, y0, x1, y1):
    """Vertical gradient: deep purple -> magenta -> orange -> gold."""
    stops = [
        (0.00, (28, 16, 58)),
        (0.38, (118, 38, 92)),
        (0.68, (224, 92, 58)),
        (1.00, (250, 178, 84)),
    ]
    height = y1 - y0
    for y in range(y0, y1):
        t = (y - y0) / max(height - 1, 1)
        for i in range(len(stops) - 1):
            t0, c0 = stops[i]
            t1, c1 = stops[i + 1]
            if t0 <= t <= t1:
                f = 0.0 if t1 == t0 else (t - t0) / (t1 - t0)
                col = lerp(c0, c1, f)
                break
        else:
            col = stops[-1][1]
        draw.line([(x0, y), (x1, y)], fill=col)


def skyline(draw, x0, y_base, x1, color):
    """Deterministic tower silhouettes with a few lit windows."""
    towers = [
        (0, 66), (46, 96), (92, 58), (138, 112), (186, 78),
        (236, 128), (288, 88), (338, 104), (388, 62), (438, 118),
        (492, 84), (544, 102), (596, 70), (648, 122), (700, 86),
        (752, 108), (804, 64), (852, 98), (900, 76),
    ]
    for dx, th in towers:
        bx0 = x0 + dx
        bx1 = min(bx0 + 44, x1)
        draw.rectangle([bx0, y_base - th, bx1, y_base], fill=color)
        for wy in range(y_base - th + 10, y_base - 8, 16):
            for wx in range(bx0 + 8, bx1 - 6, 12):
                if (wx + wy) % 3 == 0:
                    draw.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 207, 110))


def palm(draw, x, y_base, h, color):
    """One palm silhouette: gently leaning trunk, drooping fronds."""
    top_x, top_y = x + 6, y_base - h
    pts = [(x, y_base), (x + 3, y_base - h // 2), (top_x, top_y)]
    draw.line(pts, fill=color, width=5, joint="curve")
    for dx, dy in [
        (-30, 16), (-24, 26), (-8, 32), (12, 30), (28, 18),
    ]:
        mx, my = top_x + dx // 2, top_y - 10
        draw.line(
            [(top_x, top_y), (mx, my), (top_x + dx, top_y + dy)],
            fill=color, width=3, joint="curve",
        )


def draw_poster():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Outer frame.
    d.rectangle([20, 20, W - 21, H - 21], outline=INK, width=3)
    d.rectangle([27, 27, W - 28, H - 28], outline=RULE, width=1)

    # ---- Masthead ----
    f_title = font(SERIF_B, 58)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, 44), title, font=f_title, fill=INK)
    f_date = font(SANS_B, 25)
    date = "THURSDAY, 19 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 118), date, font=f_date, fill=(140, 28, 32))
    d.line([(36, 158), (W - 36, 158)], fill=INK, width=3)
    d.line([(36, 163), (W - 36, 163)], fill=INK, width=1)

    # ---- Hero: Vice City sunset ----
    hx0, hx1 = 36, W - 36
    hy0, hy1 = 172, 452
    sunset_sky(d, hx0, hy0, hx1, hy1 - 92)
    # Sun.
    d.ellipse([742, 216, 838, 312], fill=(255, 222, 140))
    d.ellipse([758, 232, 822, 296], fill=(255, 240, 190))
    # Skyline + water.
    skyline(d, hx0, hy1 - 92, hx1, (26, 14, 48))
    d.rectangle([hx0, hy1 - 92, hx1, hy1 - 88], fill=(26, 14, 48))
    for yy in range(hy1 - 88, hy1, 4):
        shade = 30 + (yy - (hy1 - 88)) * 2
        d.line([(hx0, yy), (hx1, yy)], fill=(shade, 20, 64))
    for sx in (700, 780, 860):
        d.line([(sx, hy1 - 60), (sx + 90, hy1 - 60)], fill=(255, 207, 110), width=2)
        d.line([(sx + 20, hy1 - 34), (sx + 70, hy1 - 34)], fill=(255, 207, 110), width=2)
    palm(d, 62, hy1 - 88, 84, (22, 12, 42))
    palm(d, 112, hy1 - 88, 62, (22, 12, 42))
    # Hero text strip.
    d.rectangle([hx0, hy1 - 92, hx1, hy1], fill=NAVY_DARK)
    d.rectangle([hx0, hy1 - 92, hx1, hy1 - 89], fill=GOLD, width=0)
    d.line([(hx0, hy1 - 92), (hx1, hy1 - 92)], fill=GOLD, width=3)
    f_kick = font(SANS_B, 17)
    d.text((hx0 + 18, hy1 - 84), "VICE CITY OPENS", font=f_kick, fill=GOLD_PALE)
    f_hero = font(SERIF_B, 33)
    d.text((hx0 + 18, hy1 - 58), "GTA VI launches worldwide", font=f_hero, fill=(255, 255, 255))
    f_sub = font(SANS, 18)
    d.text(
        (hx0 + 18, hy1 - 22),
        "First reviews: 99/100  ·  2.3 million watch on Twitch",
        font=f_sub, fill=(214, 222, 238),
    )

    # ---- Story grid: 2 columns x 3 rows ----
    stories = [
        ("DIPLOMACY · SHENZHEN", (26, 74, 138),
         "Trump, Xi and Putin hold first-ever trilateral talks",
         "Nuclear arms top the agenda at the APEC sidelines; no deal expected."),
        ("JUSTICE · THE HAGUE", (140, 28, 32),
         "World court delivers Rohingya genocide judgment",
         "The Gambia v. Myanmar: a first for the court, seven years on."),
        ("ASIA · JAKARTA", (16, 110, 78),
         "Indonesia passes asset-forfeiture law",
         "Corrupt assets can be seized without a conviction first."),
        ("EUROPE · TALLINN", (120, 70, 20),
         "Estonia to close border with Russia",
         "Crossings shut from December after an arson attempt on a drone maker."),
        ("MIDDLE EAST · JERUSALEM", (110, 60, 30),
         "Ex-army chief asked to form government",
         "Herzog taps Eisenkot, passing over Netanyahu."),
        ("MARKETS", (146, 110, 16),
         "Gold sinks to $3,730 an ounce",
         "A 14-month low after Fed minutes point to more rate rises."),
    ]
    col_x = [36, 524]
    row_y = [470, 612, 754]
    col_w = 464
    f_kick2 = font(SANS_B, 15)
    f_head = font(SERIF_B, 24)
    f_body = font(SANS, 17)
    for i, (kick, kcol, head, body) in enumerate(stories):
        cx = col_x[i % 2]
        cy = row_y[i // 2]
        d.rectangle([cx, cy + 4, cx + 5, cy + 122], fill=kcol)
        tx = cx + 18
        d.text((tx, cy), kick, font=f_kick2, fill=kcol)
        lines = wrap(d, head, f_head, col_w - 18)
        yy = cy + 24
        for ln in lines[:2]:
            d.text((tx, yy), ln, font=f_head, fill=INK)
            yy += 29
        blines = wrap(d, body, f_body, col_w - 18)
        for ln in blines[:2]:
            d.text((tx, yy), ln, font=f_body, fill=(58, 54, 60))
            yy += 22
        if i // 2 < 2:
            d.line([(36, cy + 130), (W - 36, cy + 130)], fill=(196, 188, 172), width=1)

    # ---- Footer ticker ----
    fy0, fy1 = 902, 986
    d.rectangle([36, fy0, W - 36, fy1], fill=NAVY)
    f_tick = font(SANS, 15)
    f_tick_b = font(SANS_B, 15)
    ticker = (
        "Four nations urge Gaza aid access  ·  Prague rallies for press freedom  ·  "
        "Spain's general strike  ·  Cyclone Akvan nears Odisha  ·  "
        "US–Philippines $2bn loan  ·  EU proposes €45bn Ukraine loan"
    )
    label = "ALSO TODAY:  "
    lw = d.textlength(label, font=f_tick_b)
    d.text((52, fy0 + 10), label, font=f_tick_b, fill=GOLD_PALE)
    tlines = wrap(d, ticker, f_tick, (W - 36 - 52) - lw - 16)
    yy = fy0 + 10
    for ln in tlines[:3]:
        d.text((52 + lw, yy), ln, font=f_tick, fill=(232, 236, 244))
        yy += 20
    # If the ticker wrapped onto a third line, it still fits: band is 84 tall.
    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    img = draw_poster()
    img.save(os.path.join(OUT, "entry.png"), format="PNG")


if __name__ == "__main__":
    main()
