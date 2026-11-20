#!/usr/bin/env python3
"""The World in One Day - Friday 20 November 2026.

Draws a complete newspaper front page (1024x1024 PNG) with PIL:
masthead, day-in-numbers strip, region count bar, three illustrated
lead stories, ten illustrated grid stories, a flat world map with the
illustrated stories pinned, a 32-item ALSO list, a DATE CHECK box and
a footer.  Data-driven: every story is a dict, scenes are painted by
name from small vector primitives.  Deterministic: no randomness, no
network, no clock.  Fonts: Liberation Serif + Liberation Sans only.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 241, 227)
INK = (26, 23, 16)
RED = (164, 32, 24)
DARKRED = (122, 22, 16)
GREY = (96, 90, 78)
RULE = (26, 23, 16)
CARD = (252, 249, 240)
WHITE = (255, 255, 255)

FD = "/usr/share/fonts/truetype/liberation/"
def F(name, size):
    return ImageFont.truetype(FD + name, size)
def SB(s): return F("LiberationSerif-Bold.ttf", s)
def SR(s): return F("LiberationSerif-Regular.ttf", s)
def SI(s): return F("LiberationSerif-Italic.ttf", s)
def NB(s): return F("LiberationSans-Bold.ttf", s)
def NR(s): return F("LiberationSans-Regular.ttf", s)
def NI(s): return F("LiberationSans-Italic.ttf", s)

def tw(d, s, font):
    return d.textlength(s, font=font)

def wrap(d, s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(d, t, font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def spaced(d, xy, s, font, fill, gap=2):
    x, y = xy
    for ch in s:
        d.text((x, y), ch, font=font, fill=fill)
        x += tw(d, ch, font) + gap
    return x - gap

def spaced_w(d, s, font, gap=2):
    return sum(tw(d, ch, font) + gap for ch in s) - gap

def chip(d, box, s, bgc, fgc=None, font=None):
    font = font or NB(11)
    fgc = fgc or WHITE
    w_ = tw(d, s, font) + 14
    x0, y0 = box
    d.rounded_rectangle([x0, y0, x0 + w_, y0 + 20], 4, fill=bgc)
    d.text((x0 + 7, y0 + 4), s, font=font, fill=fgc)
    return w_

# ---------------------------------------------------------------- scenes
def scene_base(w_, h_, top, bot):
    img = Image.new("RGB", (w_, h_), top)
    dd = ImageDraw.Draw(img)
    for i in range(h_):
        t = i / max(1, h_ - 1)
        dd.line([(0, i), (w_, i)], fill=tuple(
            int(top[c] + (bot[c] - top[c]) * t) for c in range(3)))
    return img, dd

def sc_cyclone(w_, h_):
    img, d = scene_base(w_, h_, (16, 52, 74), (30, 92, 110))
    cx, cy = int(w_ * 0.34), int(h_ * 0.46)
    for r in (52, 40, 29, 19):
        d.arc([cx - r, cy - r * 0.72, cx + r, cy + r * 0.72], 300, 130, fill=(210, 232, 238), width=5)
        d.arc([cx - r, cy - r * 0.72, cx + r, cy + r * 0.72], 120, 300, fill=(160, 205, 218), width=4)
    d.ellipse([cx - 8, cy - 6, cx + 8, cy + 6], fill=(238, 246, 248))
    d.polygon([(int(w_ * 0.62), h_), (int(w_ * 0.78), int(h_ * 0.30)),
               (int(w_ * 0.92), int(h_ * 0.42)), (w_, int(h_ * 0.55)), (w_, h_)],
              fill=(196, 172, 120))
    d.line([(int(w_ * 0.62), h_), (int(w_ * 0.78), int(h_ * 0.30)),
            (int(w_ * 0.92), int(h_ * 0.42)), (w_, int(h_ * 0.55))], fill=(230, 214, 160), width=2)
    for i in range(9):
        x = int(w_ * 0.55) + i * 16
        d.line([(x, 6), (x - 7, 22)], fill=(170, 215, 228), width=2)
    for i in range(4):
        y = int(h_ * 0.72) + i * 7
        d.arc([int(w_ * 0.06), y, int(w_ * 0.30), y + 12], 180, 330, fill=(190, 224, 232), width=2)
    chip(d, (w_ - 118, h_ - 28), "GUSTS 110 KM/H", (10, 30, 44))
    return img

def sc_missiles(w_, h_):
    img, d = scene_base(w_, h_, (10, 14, 38), (34, 38, 74))
    for (sx, sy, sr) in [(30, 18, 2), (90, 30, 1), (150, 12, 2), (230, 26, 1), (300, 16, 2), (60, 44, 1), (200, 48, 1)]:
        if sx < w_:
            d.ellipse([sx, sy, sx + sr * 2, sy + sr * 2], fill=(220, 224, 240))
    gy = int(h_ * 0.78)
    for bx, bw, bh in [(0, 42, 34), (46, 30, 48), (80, 52, 28), (136, 34, 56), (174, 46, 36),
                       (224, 30, 50), (258, 54, 30), (316, 36, 44)]:
        if bx < w_:
            d.rectangle([bx, gy - bh, bx + bw, gy], fill=(16, 18, 34))
            for wy in range(gy - bh + 6, gy - 6, 10):
                for wx in range(bx + 5, bx + bw - 5, 11):
                    if (wx * 7 + wy * 13) % 5 < 2:
                        d.rectangle([wx, wy, wx + 4, wy + 5], fill=(250, 205, 92))
    d.rectangle([0, gy, w_, h_], fill=(12, 12, 26))
    for tx, col in [(int(w_ * 0.30), (255, 150, 60)), (int(w_ * 0.62), (255, 120, 50))]:
        for r in (16, 10, 5):
            d.ellipse([tx - r, gy - 6 - r, tx + r, gy - 6 + r], fill=col if r == 5 else (200, 80, 40))
        d.line([(tx - 26, gy - 44), (tx, gy - 8)], fill=(255, 190, 110), width=2)
        d.line([(tx + 30, gy - 50), (tx + 2, gy - 8)], fill=(255, 190, 110), width=2)
    for i, fx in enumerate(range(int(w_ * 0.14), w_, 76)):
        fy = gy - 62 - (i % 3) * 14
        d.line([(fx - 30, fy - 18), (fx + 26, fy + 10)], fill=(240, 200, 130), width=2)
        d.ellipse([fx + 24, fy + 8, fx + 30, fy + 14], fill=(255, 220, 150))
    chip(d, (10, 8), "01:25 LOCAL - 7 WAVES", (88, 16, 12))
    chip(d, (w_ - 96, 8), "~30 MISSILES", (240, 238, 230), INK)
    return img

def sc_cop31(w_, h_):
    img, d = scene_base(w_, h_, (238, 226, 196), (214, 188, 150))
    d.ellipse([int(w_ * 0.06), 10, int(w_ * 0.06) + 34, 44], fill=(240, 176, 64))
    for bx, bw, bh in [(0, 60, 30), (66, 44, 42), (116, 70, 26), (250, 52, 38), (308, 60, 28)]:
        if bx < w_:
            d.rectangle([bx, h_ - bh, bx + bw, h_], fill=(120, 96, 74))
            d.polygon([(bx, h_ - bh), (bx + bw // 2, h_ - bh - 10), (bx + bw, h_ - bh)], fill=(92, 70, 52))
    gx, gy, gr = int(w_ * 0.60), int(h_ * 0.44), 30
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(64, 128, 168))
    d.polygon([(gx - 20, gy - 12), (gx - 4, gy - 18), (gx - 2, gy - 4), (gx - 16, gy + 2)], fill=(96, 168, 96))
    d.polygon([(gx + 4, gy + 6), (gx + 20, gy + 2), (gx + 22, gy + 16), (gx + 8, gy + 18)], fill=(96, 168, 96))
    tx = int(w_ * 0.80)
    d.rounded_rectangle([tx, 12, tx + 16, h_ - 26], 8, outline=(164, 32, 24), width=3)
    d.rectangle([tx + 5, int(h_ * 0.52), tx + 11, h_ - 28], fill=(164, 32, 24))
    d.ellipse([tx - 5, h_ - 34, tx + 21, h_ - 8], outline=(164, 32, 24), width=3)
    d.rectangle([tx + 2, h_ - 28, tx + 14, h_ - 14], fill=(164, 32, 24))
    chip(d, (10, h_ - 28), "FINAL DAY - DEADLOCK", (122, 22, 16))
    chip(d, (int(w_ * 0.36), 8), "$120BN FINANCE GAP", (26, 23, 16))
    return img

def sc_selloff(w_, h_):
    img, d = scene_base(w_, h_, (24, 22, 30), (40, 30, 40))
    for gx in range(20, w_, 34):
        d.line([(gx, 6), (gx, h_ - 6)], fill=(58, 54, 66), width=1)
    for gy in range(10, h_, 20):
        d.line([(6, gy), (w_ - 6, gy)], fill=(58, 54, 66), width=1)
    pts = [(8, int(h_ * 0.22)), (int(w_ * 0.22), int(h_ * 0.30)), (int(w_ * 0.40), int(h_ * 0.26)),
           (int(w_ * 0.56), int(h_ * 0.48)), (int(w_ * 0.72), int(h_ * 0.55)), (int(w_ * 0.90), int(h_ * 0.78))]
    d.line(pts, fill=(232, 64, 48), width=3)
    for (px, py) in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 120, 100))
    ax, ay = pts[-1]
    d.polygon([(ax, ay + 12), (ax - 10, ay - 2), (ax + 10, ay - 2)], fill=(232, 64, 48))
    chip(d, (8, 8), "ASIA -7% WK", (164, 32, 24))
    return img

def sc_mercury(w_, h_):
    img, d = scene_base(w_, h_, (4, 6, 16), (10, 12, 28))
    for (sx, sy, sr) in [(20, 14, 2), (70, 30, 1), (130, 10, 2), (180, 36, 1), (40, 52, 1), (230, 16, 2), (270, 44, 1), (110, 50, 1)]:
        if sx < w_:
            d.ellipse([sx, sy, sx + sr * 2, sy + sr * 2], fill=(210, 214, 230))
    px, py, pr = int(w_ * 0.72), int(h_ * 0.56), 26
    d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(168, 160, 148))
    for (ox, oy, orad) in [(-10, -6, 6), (8, 4, 8), (0, 14, 4), (14, -12, 5)]:
        d.ellipse([px + ox - orad, py + oy - orad, px + ox + orad, py + oy + orad], outline=(130, 122, 110), width=2)
    d.arc([px - pr - 16, py - 14, px + pr + 16, py + 14], 20, 160, fill=(120, 140, 180), width=2)
    bx, by = int(w_ * 0.28), int(h_ * 0.44)
    d.rectangle([bx - 7, by - 7, bx + 7, by + 7], fill=(216, 178, 84))
    d.polygon([(bx - 34, by - 12), (bx - 10, by - 4), (bx - 10, by + 4), (bx - 34, by + 12)], fill=(70, 110, 190))
    d.polygon([(bx + 34, by - 12), (bx + 10, by - 4), (bx + 10, by + 4), (bx + 34, by + 12)], fill=(70, 110, 190))
    d.line([(bx, by + 7), (bx, by + 20)], fill=(200, 200, 210), width=2)
    d.ellipse([bx - 6, by + 18, bx + 6, by + 28], outline=(200, 200, 210), width=2)
    chip(d, (8, 8), "6BN MILES", (40, 44, 70))
    return img

def sc_eudeal(w_, h_):
    img, d = scene_base(w_, h_, (24, 44, 96), (36, 62, 128))
    import math
    cx, cy = int(w_ * 0.24), int(h_ * 0.48)
    for i in range(12):
        a = math.radians(i * 30 - 90)
        sx, sy = cx + int(22 * math.cos(a)), cy + int(22 * math.sin(a))
        d.polygon([(sx, sy - 5), (sx + 2, sy), (sx + 5, sy), (sx + 2, sy + 2), (sx + 3, sy + 5),
                   (sx, sy + 3), (sx - 3, sy + 5), (sx - 2, sy + 2), (sx - 5, sy), (sx - 2, sy)],
                  fill=(250, 205, 60))
    fx, fy, fw, fh = int(w_ * 0.52), int(h_ * 0.16), int(w_ * 0.40), int(h_ * 0.62)
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(38, 60, 140))
    d.polygon([(fx, fy), (fx + fw, fy + fh)], fill=(230, 230, 230), width=0)
    d.line([(fx, fy), (fx + fw, fy + fh)], fill=(230, 230, 230), width=7)
    d.line([(fx + fw, fy), (fx, fy + fh)], fill=(230, 230, 230), width=7)
    d.line([(fx, fy), (fx + fw, fy + fh)], fill=(178, 30, 40), width=3)
    d.line([(fx + fw, fy), (fx, fy + fh)], fill=(178, 30, 40), width=3)
    d.rectangle([fx + fw // 2 - 5, fy, fx + fw // 2 + 5, fy + fh], fill=(230, 230, 230))
    d.rectangle([fx, fy + fh // 2 - 5, fx + fw, fy + fh // 2 + 5], fill=(230, 230, 230))
    d.rectangle([fx + fw // 2 - 3, fy, fx + fw // 2 + 3, fy + fh], fill=(178, 30, 40))
    d.rectangle([fx, fy + fh // 2 - 3, fx + fw, fy + fh // 2 + 3], fill=(178, 30, 40))
    ex, ey = int(w_ * 0.30), int(h_ * 0.80)
    d.polygon([(ex, ey), (ex + 44, ey), (ex + 22, ey + 12)], fill=(240, 236, 224))
    d.rectangle([ex, ey - 14, ex + 44, ey], outline=(240, 236, 224), width=2)
    chip(d, (8, h_ - 24), "RESET DEAL", (10, 22, 52))
    return img

def sc_inflation(w_, h_):
    img, d = scene_base(w_, h_, (250, 246, 238), (238, 228, 210))
    base = h_ - 14
    for i, bh in enumerate((14, 20, 26, 36)):
        bx = 14 + i * 26
        d.rectangle([bx, base - bh, bx + 18, base], fill=(164, 32, 24) if i == 3 else (90, 90, 100))
    d.line([(10, base - 8), (int(w_ * 0.55), base - 42)], fill=(26, 23, 16), width=2)
    d.polygon([(int(w_ * 0.55), base - 42), (int(w_ * 0.55) - 9, base - 38), (int(w_ * 0.55) - 3, base - 31)], fill=(26, 23, 16))
    cx, cy = int(w_ * 0.78), int(h_ * 0.42)
    d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(240, 196, 76), outline=(178, 138, 40), width=3)
    d.text((cx - 6, cy - 11), "¥", font=NB(20), fill=(120, 90, 20))
    chip(d, (8, 6), "CPI 2.3%", (26, 23, 16))
    return img

def sc_rates(w_, h_):
    img, d = scene_base(w_, h_, (146, 30, 28), (110, 22, 22))
    bx, by, bw = int(w_ * 0.16), int(h_ * 0.30), int(w_ * 0.68)
    d.polygon([(bx - 8, by), (bx + bw // 2, by - 16), (bx + bw + 8, by)], fill=(240, 230, 210))
    for i in range(4):
        cx = bx + 8 + i * (bw - 16) // 3 - 4
        d.rectangle([cx, by + 4, cx + 8, by + 30], fill=(240, 230, 210))
    d.rectangle([bx - 6, by + 34, bx + bw + 6, by + 40], fill=(240, 230, 210))
    chip(d, (8, 6), "18TH MONTH", (70, 12, 10))
    chip(d, (w_ - 104, h_ - 24), "3.0% / 3.5%", (240, 238, 230), INK)
    return img

def sc_cricket(w_, h_):
    img, d = scene_base(w_, h_, (52, 120, 62), (38, 96, 48))
    d.rectangle([0, 0, w_, int(h_ * 0.30)], fill=(30, 60, 96))
    for i in range(6):
        d.rectangle([8 + i * (w_ // 6), int(h_ * 0.10), 8 + i * (w_ // 6) + w_ // 9, int(h_ * 0.28)], fill=(52, 84, 124))
    px = int(w_ * 0.40)
    d.rectangle([px, int(h_ * 0.34), px + int(w_ * 0.20), h_ - 6], fill=(214, 196, 150))
    for sx in (px + 8, px + int(w_ * 0.20) - 12):
        for k in range(3):
            d.rectangle([sx + k * 4, int(h_ * 0.44), sx + k * 4 + 2, int(h_ * 0.44) + 16], fill=(240, 230, 200))
    d.line([(px + int(w_ * 0.30), int(h_ * 0.80)), (px + int(w_ * 0.42), int(h_ * 0.52))], fill=(120, 84, 40), width=4)
    d.ellipse([px + int(w_ * 0.46), int(h_ * 0.48), px + int(w_ * 0.46) + 8, int(h_ * 0.48) + 8], fill=(178, 30, 40))
    chip(d, (8, 6), "118 - RECORD", (16, 52, 26))
    return img

def sc_bukele(w_, h_):
    img, d = scene_base(w_, h_, (120, 180, 225), (190, 215, 240))
    fx, fy, fw, fh = int(w_ * 0.10), 8, int(w_ * 0.44), int(h_ * 0.52)
    d.rectangle([fx, fy, fx + fw, fy + fh // 3], fill=(40, 80, 160))
    d.rectangle([fx, fy + fh // 3, fx + fw, fy + 2 * fh // 3], fill=(245, 245, 245))
    d.rectangle([fx, fy + 2 * fh // 3, fx + fw, fy + fh], fill=(40, 80, 160))
    d.ellipse([fx + fw // 2 - 7, fy + fh // 2 - 7, fx + fw // 2 + 7, fy + fh // 2 + 7], fill=(90, 160, 200), outline=(40, 80, 160))
    d.line([(fx, fy), (fx, h_ - 4)], fill=(90, 70, 50), width=3)
    bx, by = int(w_ * 0.62), int(h_ * 0.52)
    d.rectangle([bx, by, bx + 52, by + 30], fill=(240, 238, 230), outline=(26, 23, 16), width=2)
    d.rectangle([bx + 10, by - 6, bx + 42, by], fill=(26, 23, 16))
    d.line([(bx + 18, by + 15), (bx + 25, by + 22), (bx + 38, by + 7)], fill=(164, 32, 24), width=3)
    chip(d, (8, h_ - 24), "THIRD TERM", (24, 52, 100))
    return img

def sc_boat(w_, h_):
    img, d = scene_base(w_, h_, (30, 80, 120), (22, 58, 96))
    for wy in range(int(h_ * 0.55), h_, 9):
        for wx in range(0, w_, 36):
            d.arc([wx + (wy % 18), wy, wx + 26 + (wy % 18), wy + 8], 180, 340, fill=(140, 200, 225), width=2)
    hx, hy = int(w_ * 0.40), int(h_ * 0.52)
    d.polygon([(hx - 44, hy), (hx + 44, hy), (hx + 26, hy - 16), (hx - 26, hy - 16)], fill=(150, 60, 40))
    d.line([(hx - 10, hy - 16), (hx + 6, hy - 40)], fill=(220, 210, 190), width=3)
    for (px, py) in [(hx - 58, hy + 10), (hx + 56, hy + 6), (hx + 20, hy + 16)]:
        d.ellipse([px - 4, py - 10, px + 4, py - 2], fill=(240, 200, 160))
        d.arc([px - 6, py - 2, px + 6, py + 8], 0, 180, fill=(240, 200, 160), width=3)
    rx = int(w_ * 0.84)
    d.polygon([(rx - 26, int(h_ * 0.72)), (rx + 26, int(h_ * 0.72)), (rx + 16, int(h_ * 0.60)), (rx - 16, int(h_ * 0.60))], fill=(245, 245, 245))
    d.rectangle([rx - 3, int(h_ * 0.44), rx + 3, int(h_ * 0.60)], fill=(164, 32, 24))
    chip(d, (8, 6), "4 DEAD", (90, 20, 14))
    return img

def sc_strike(w_, h_):
    img, d = scene_base(w_, h_, (228, 214, 188), (206, 188, 158))
    for bx, bw, bh in [(0, 40, 44), (46, 34, 58), (86, 48, 40), (190, 40, 52), (236, 44, 42)]:
        if bx < w_:
            d.rectangle([bx, h_ - 18 - bh, bx + bw, h_ - 18], fill=(150, 128, 100))
    gy = h_ - 16
    for i, px in enumerate(range(12, w_ - 8, 22)):
        py = gy - 14 - (i % 2) * 3
        d.ellipse([px - 4, py - 8, px + 4, py], fill=(52, 42, 34))
        d.rectangle([px - 4, py, px + 4, gy], fill=(52, 42, 34) if i % 3 else (164, 32, 24))
        if i % 3 == 0:
            d.line([(px + 4, py + 2), (px + 16, py - 12)], fill=(90, 70, 50), width=2)
            d.rectangle([px + 16, py - 22, px + 40, py - 12], fill=(200, 44, 36))
    chip(d, (8, 6), "24-HR STRIKE", (122, 22, 16))
    return img

def sc_pill(w_, h_):
    img, d = scene_base(w_, h_, (18, 62, 66), (14, 46, 52))
    cx, cy = int(w_ * 0.36), int(h_ * 0.50)
    d.rounded_rectangle([cx - 44, cy - 16, cx + 44, cy + 16], 16, fill=(240, 238, 230))
    d.rounded_rectangle([cx, cy - 16, cx + 44, cy + 16], 16, fill=(200, 44, 48))
    d.line([(cx, cy - 16), (cx, cy + 16)], fill=(160, 160, 160), width=2)
    for (tx, ty, tr, col) in [(int(w_ * 0.74), int(h_ * 0.34), 13, (232, 120, 110)),
                              (int(w_ * 0.84), int(h_ * 0.62), 8, (240, 170, 160)),
                              (int(w_ * 0.68), int(h_ * 0.70), 5, (250, 210, 200))]:
        d.ellipse([tx - tr, ty - tr, tx + tr, ty + tr], outline=col, width=3)
        d.line([(tx - tr + 3, ty), (tx + tr - 3, ty)], fill=col, width=2)
    chip(d, (8, 6), "60.7% RESPONSE", (8, 34, 36))
    return img

SCENES = {
    "cyclone": sc_cyclone, "missiles": sc_missiles, "cop31": sc_cop31,
    "selloff": sc_selloff, "mercury": sc_mercury, "eudeal": sc_eudeal,
    "inflation": sc_inflation, "rates": sc_rates, "cricket": sc_cricket,
    "bukele": sc_bukele, "boat": sc_boat, "strike": sc_strike, "pill": sc_pill,
}

# ------------------------------------------------------------------- map
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70), (-80, 73), (-75, 68), (-65, 60), (-55, 52), (-60, 46), (-70, 44), (-75, 40), (-76, 35), (-80, 32), (-81, 26), (-84, 20), (-90, 21), (-97, 16), (-105, 20), (-110, 24), (-114, 29), (-120, 34), (-124, 40), (-124, 46), (-130, 55), (-150, 60), (-165, 60)],
    [(-79, 9), (-72, 12), (-64, 10), (-55, 6), (-50, 0), (-44, -3), (-35, -8), (-39, -13), (-41, -22), (-48, -27), (-52, -33), (-58, -39), (-62, -41), (-65, -45), (-67, -50), (-68, -54), (-71, -54), (-73, -46), (-73, -37), (-71, -30), (-70, -20), (-75, -15), (-79, -8), (-81, -4), (-80, 1), (-77, 4)],
    [(-17, 15), (-10, 29), (-6, 35), (10, 37), (11, 34), (20, 32), (30, 31), (35, 28), (38, 22), (43, 12), (51, 12), (48, 5), (42, -5), (40, -15), (36, -22), (33, -26), (28, -33), (20, -35), (17, -32), (14, -22), (12, -15), (13, -5), (9, 4), (-8, 4), (-13, 8), (-17, 12)],
    [(-9, 43), (-2, 44), (-1, 46), (-5, 48), (0, 49), (2, 51), (5, 53), (8, 55), (8, 57), (10, 59), (18, 56), (21, 55), (24, 58), (28, 59), (30, 60), (25, 66), (20, 70), (30, 70), (40, 68), (45, 66), (40, 64), (35, 65), (32, 60), (28, 55), (23, 52), (18, 50), (14, 48), (10, 45), (12, 44), (15, 42), (18, 40), (15, 38), (12, 38), (10, 37), (3, 37), (-2, 37), (-6, 36), (-9, 37), (-9, 43)],
    [(-5, 50), (-3, 53), (-5, 55), (-3, 58), (-6, 58), (-8, 55), (-6, 52), (-5, 51)],
    [(40, 68), (60, 69), (80, 73), (100, 77), (120, 73), (140, 72), (160, 70), (178, 66), (178, 62), (160, 55), (142, 50), (140, 40), (135, 35), (127, 40), (122, 38), (120, 32), (115, 23), (108, 15), (105, 9), (100, 7), (98, 12), (95, 16), (92, 16), (89, 22), (86, 20), (80, 15), (77, 8), (72, 20), (66, 25), (61, 25), (57, 27), (52, 28), (48, 30), (44, 29), (40, 31), (36, 36), (36, 42), (40, 45), (40, 50), (38, 55), (40, 68)],
    [(113, -22), (114, -28), (115, -34), (118, -35), (124, -33), (129, -32), (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (151, -24), (146, -19), (142, -11), (142, -15), (139, -17), (136, -15), (135, -12), (132, -11), (130, -13), (126, -14), (122, -17), (118, -20)],
    [(167, -45), (171, -41), (174, -39), (176, -38), (174, -41), (172, -43), (169, -46), (167, -45)],
]

def draw_map(d, box, pins):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(24, 34, 52))
    def proj(lon, lat):
        return (x0 + (lon + 180) / 360 * (x1 - x0), y0 + (90 - lat) / 180 * (y1 - y0))
    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=(196, 172, 120))
    for lon, lat in [(100, -2), (110, -3), (120, -2), (131, -3), (141, -4)]:
        px, py = proj(lon, lat)
        d.ellipse([px - 5, py - 2, px + 5, py + 2], fill=(196, 172, 120))
    for lon, lat in [(130, 31), (137, 35), (141, 40), (142, 44)]:
        px, py = proj(lon, lat)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(196, 172, 120))
    pin_off = {1: (33, 53), 3: (34, 33), 6: (5, 53), 12: (16, 40), 13: (-1, 44)}
    for num, lon, lat in pins:
        lon, lat = pin_off.get(num, (lon, lat))
        px, py = proj(lon, lat)
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=WHITE, width=2)
        s = str(num)
        fnt = NB(10 if len(s) < 2 else 9)
        d.text((px - tw(d, s, fnt) / 2, py - 6), s, font=fnt, fill=WHITE)
    d.text((x0 + 8, y1 - 18), "SPACE: 5 Mercury", font=NB(9), fill=(200, 214, 235))

# ------------------------------------------------------------------ data
LEADS = [
    dict(n=1, scene="missiles", place="KYIV, UKRAINE", beat="WAR", tag="Officials say",
         head="Russia fires wave of ~30 ballistic missiles at Kyiv",
         deck="Seven overnight waves hit energy and transport sites; fires burn in three districts and the Dutch and Austrian embassies are damaged, city officials say. (Kyiv Post, Reuters)",
         pin=(30.52, 50.45)),
    dict(n=2, scene="cyclone", place="ODISHA, INDIA", beat="CYCLONE", tag="IMD",
         head="Cyclone Akvan makes landfall in eastern India",
         deck="The severe storm crosses near Gopalpur; 300,000+ evacuated, winds 90-100 gusting 110 km/h, 423 rescue teams deployed and schools shut. (IMD, The Hindu)",
         pin=(84.92, 19.27)),
    dict(n=3, scene="cop31", place="ANTALYA, TURKIYE", beat="CLIMATE", tag="UN News",
         head="COP31 reaches its final day deadlocked",
         deck="The closing draft omits a fossil-fuel phase-out while a $120bn adaptation finance gap stays unresolved; hosts push a '35 by 35' clean-power goal. (UN News, Reuters)",
         pin=(30.71, 36.88)),
]

GRID = [
    dict(n=4, scene="selloff", place="SEOUL / TOKYO", beat="MARKETS", tag="Reuters",
         head="AI sell-off sinks Asia to worst week since 2020",
         deck="Nikkei -4.5%, KOSPI -4.7%, SoftBank -16%; MSCI Asia-Pacific down 7%. (Reuters)",
         pin=(126.98, 37.57)),
    dict(n=5, scene="mercury", place="MERCURY", beat="SPACE", tag="ESA",
         head="BepiColombo reaches Mercury after 8 years",
         deck="ESA/JAXA probe ends a 6bn-mile trip; orbit insertion Saturday. (ESA, BBC)",
         pin=None),
    dict(n=6, scene="eudeal", place="BRUSSELS", beat="EUROPE", tag="Reported",
         head="UK and EU seal 'reset' deal a decade after Brexit",
         deck="Youth mobility, food trade, carbon links; food deal GBP 5.1bn. (Al Jazeera)",
         pin=(4.35, 50.85)),
    dict(n=7, scene="inflation", place="TOKYO", beat="ECONOMY", tag="Reuters",
         head="Japan inflation hits 2.3%; BoJ hike eyed",
         deck="October headline CPI rises from 2.1%; core stays above 2% for a second month. (Reuters)",
         pin=(139.69, 35.68)),
    dict(n=8, scene="rates", place="BEIJING", beat="RATES", tag="PBOC",
         head="China holds lending rates for 18th month",
         deck="1-year LPR at 3.0%, 5-year at 3.5%, as expected. (PBOC, Reuters)",
         pin=(116.40, 39.90)),
    dict(n=9, scene="cricket", place="WELLINGTON", beat="CRICKET", tag="ICC",
         head="Phillips makes history with 118 vs India",
         deck="First NZ batter with centuries in all 3 formats vs India in a year. (ICC)",
         pin=(174.78, -41.29)),
    dict(n=10, scene="bukele", place="SAN SALVADOR", beat="POLITICS", tag="AP",
         head="Bukele registers for a third term",
         deck="Files with the tribunal for the Feb 2027 vote; rights groups object. (AP)",
         pin=(-89.22, 13.69)),
    dict(n=11, scene="boat", place="SENEGAL", beat="MIGRATION", tag="Al Jazeera",
         head="Migrant boat capsizes off Yenne; 4 dead",
         deck="Dozens are missing from 50-100 aboard, as Canary Islands arrivals surge. (Al Jazeera)",
         pin=(-17.35, 14.55)),
    dict(n=12, scene="strike", place="ROME", beat="LABOUR", tag="AFP",
         head="Italy's CGIL holds 24-hour general strike",
         deck="Unions rally in 100 squares against the 2027 budget; transit hit. (CGIL, AFP)",
         pin=(12.50, 41.90)),
    dict(n=13, scene="pill", place="BARCELONA", beat="HEALTH", tag="Reuters",
         head="Pancreatic cancer pill shrinks tumours 60.7%",
         deck="Daraxonrasib plus chemo beats chemo alone (23-42%) in an early trial. (Reuters)",
         pin=(2.17, 41.38)),
]

ALSO = [
    (14, "WASHINGTON", "Pentagon puts the US war cost against Iran at $48.3bn (Reuters)"),
    (15, "NEW YORK", "Mamdani plans to close Rikers Island jail by 2032 (reports)"),
    (16, "MEXICO CITY", "The nation marks its 116th Revolution Day (AP)"),
    (17, "PORT-AU-PRINCE", "Police say a raid killed 34 gang suspects (Reuters)"),
    (18, "LAS VEGAS", "Russell is fastest in wet Las Vegas Grand Prix practice, 1:47.272 (Formula1.com)"),
    (19, "FLORIDA", "St Johns River hits a record 18.3 ft; four counties shut schools (AP)"),
    (20, "SAO PAULO", "Markets shut for Black Consciousness Day (AFP)"),
    (21, "LONDON", "UK and Norway fund GBP 100m+ for two Ukrainian naval vessels (BBC)"),
    (22, "COPENHAGEN", "Denmark's parliament approves the Greenland defence bill (AFP)"),
    (23, "LUBLIN", "A Russian cruise missile lands in a Polish field; Tusk calls it a provocation (officials say)"),
    (24, "BERLIN", "Young Germans rally against conscription in many cities (reported)"),
    (25, "TURIN", "Alcaraz-Cobolli and Medvedev-Tiafoe close the ATP Finals groups (ATP)"),
    (26, "SMOLENSK", "Drones are reported to hit a Russian chemical plant - an unconfirmed claim (Kyiv Independent)"),
    (27, "SEOUL", "The ruling party moves to impeach Chief Justice Cho Hee-dae (SBS)"),
    (28, "SEOUL", "111 students are caught cheating in the Suneung exam (officials say)"),
    (29, "SHENZHEN", "Xi hails a 'full turnaround' in ties with Australia (CGTN, AAP)"),
    (30, "COX'S BAZAR", "Rohingya weep and pray in the camps after the ICJ ruling (Al Jazeera)"),
    (31, "HORMUZ", "The strait stays shut; Brent crude nears $92.50 and 46 ships wait (tracker reports)"),
    (32, "SAUDI ARABIA", "The coalition says it downed a Houthi missile - a claim (Reuters)"),
    (33, "BLANTYRE", "Malawi's fuel crisis: night queues and a 20-litre daily cap (Al Jazeera)"),
    (34, "BOUGAINVILLE", "Rio Tinto pledges $370m for the Panguna mine fleet (Reuters)"),
    (35, "CANBERRA", "The CBO warns AUKUS sub sales could shrink the US fleet (Reuters)"),
    (36, "TONGA", "The Pacific kingdom declares an emergency as El Nino drought bites (RNZ)"),
    (37, "JAKARTA", "Indonesia's parliament passes the asset-forfeiture bill (Reuters)"),
    (38, "NEW DELHI", "A Pakistan minister leads a delegation to the SCO dialogue (The Hindu)"),
    (39, "HONG KONG", "The Badminton Open reaches its semi-finals after an upset (BWF)"),
    (40, "KHARKIV", "A drone hits a hospital; at least four people are hurt (Ukrinform)"),
    (41, "GAZA", "Over 85% of civil defence vehicles are out of service (reports)"),
    (42, "DAKAR", "President Faye enacts a supplementary budget by decree (AFP)"),
    (43, "GLOBAL", "The UN marks World Children's Day across member states (UN News)"),
    (44, "CALIFORNIA", "The state probes Nvidia over chips in China (inquiry)"),
    (45, "WELLINGTON", "Henry Nicholls scores 175* in a 216-run stand with Phillips (ICC)"),
]

NUMBERS = [
    ("300,000+", "evacuated ahead of Cyclone Akvan"),
    ("~30", "ballistic missiles fired at Kyiv"),
    ("-7%", "Asia shares' worst week since 2020"),
    ("2.3%", "Japan Oct headline CPI; BoJ eyed"),
    ("118", "Phillips' historic century vs India"),
    ("8 yrs", "BepiColombo reaches Mercury"),
]

REGIONS = [
    ("EUROPE 12", 12, (43, 76, 126)),
    ("AMERICAS 9", 9, (179, 84, 63)),
    ("ASIA-PACIFIC 11", 11, (38, 110, 104)),
    ("MIDEAST 3", 3, (176, 128, 44)),
    ("AFRICA 3", 3, (84, 118, 60)),
    ("OCEANIA 5", 5, (110, 84, 140)),
    ("WORLD 2", 2, (60, 60, 70)),
]

DATECHECK = ("First reported Thursday 19 Nov, so NOT shown as Friday's news: the Trump-Xi-Putin "
             "Shenzhen summit itself - Anthropic's $83 IPO pricing and Nasdaq debut - the ICJ's Myanmar "
             "Rohingya genocide verdict - GTA VI's midnight launch - Voyager 1's one light-day "
             "confirmation - the Senate's 48-51 Iran war-powers vote - Fiona the hippo's death.")

# ---------------------------------------------------------------- layout
def lead_card(img, x, y, w_, h_, st):
    x, y, w_, h_ = int(x), int(y), int(w_), int(h_)
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w_, y + h_], fill=CARD, outline=(190, 180, 156), width=1)
    sc = SCENES[st["scene"]](w_ - 16, 92)
    img.paste(sc, (x + 8, y + 8))
    cy = y + 108
    kick = "%02d - %s - %s" % (st["n"], st["place"], st["beat"])
    spaced(d, (x + 10, cy), kick, NB(10), RED, gap=1)
    tagw = tw(d, st["tag"], NI(9))
    d.text((x + w_ - 10 - tagw, cy + 1), st["tag"], font=NI(9), fill=GREY)
    cy += 16
    for ln in wrap(d, st["head"], SB(19), w_ - 20)[:3]:
        d.text((x + 10, cy), ln, font=SB(19), fill=INK)
        cy += 22
    cy += 2
    for ln in wrap(d, st["deck"], NR(10), w_ - 20)[:4]:
        d.text((x + 10, cy), ln, font=NR(10), fill=(52, 48, 40))
        cy += 12

def grid_card(img, x, y, w_, h_, st):
    x, y, w_, h_ = int(x), int(y), int(w_), int(h_)
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w_, y + h_], fill=CARD, outline=(190, 180, 156), width=1)
    sc = SCENES[st["scene"]](w_ - 12, 46)
    img.paste(sc, (x + 6, y + 6))
    cy = y + 58
    kick = "%02d - %s - %s" % (st["n"], st["place"], st["beat"])
    d.text((x + 8, cy), kick, font=NB(8), fill=RED)
    cy += 11
    for ln in wrap(d, st["head"], SB(12), w_ - 16)[:2]:
        d.text((x + 8, cy), ln, font=SB(12), fill=INK)
        cy += 15
    cy += 1
    for ln in wrap(d, st["deck"], NR(9), w_ - 16)[:2]:
        d.text((x + 8, cy), ln, font=NR(9), fill=(52, 48, 40))
        cy += 11

def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    L, R = 18, 1006
    # masthead
    spaced(d, (L, 8), "THE WORLD IN ONE DAY", NB(11), RED, gap=2)
    rtxt = "ONE PAGE - 45 STORIES - 7 REGIONS"
    spaced(d, (R - spaced_w(d, rtxt, NB(11), 2), 8), rtxt, NB(11), INK, gap=2)
    title = "Friday 20 November 2026"
    tf = SB(50)
    d.text(((W - tw(d, title, tf)) / 2, 24), title, font=tf, fill=INK)
    sub = "Cyclone Akvan strikes India - Ballistic missiles hit Kyiv - COP31 deadlocked on final day - Asian AI sell-off"
    sf = SI(15)
    d.text(((W - tw(d, sub, sf)) / 2, 80), sub, font=sf, fill=DARKRED)
    d.line([(L, 102), (R, 102)], fill=RULE, width=3)
    d.line([(L, 107), (R, 107)], fill=RULE, width=1)
    # numbers strip
    ny, nh = 112, 44
    cw = (R - L) / 6
    for i, (num, cap) in enumerate(NUMBERS):
        x = L + i * cw
        if i: d.line([(x, ny + 4), (x, ny + nh - 4)], fill=(200, 190, 168), width=1)
        d.rectangle([x + (0 if i == 0 else 8), ny, x + (2 if i == 0 else 10), ny + nh], fill=RED)
        px = x + (8 if i == 0 else 16)
        d.text((px, ny), num, font=SB(22), fill=INK)
        for j, ln in enumerate(wrap(d, cap, NR(9), cw - 22)[:2]):
            d.text((px, ny + 27 + j * 11), ln, font=NR(9), fill=GREY)
    d.line([(L, ny + nh + 4), (R, ny + nh + 4)], fill=(200, 190, 168), width=1)
    # region bar
    by = ny + nh + 8
    total = sum(c for _, c, _ in REGIONS)
    x = L
    for label, cnt, col in REGIONS:
        segw = (R - L) * cnt / total
        d.rectangle([x, by, x + segw - 2, by + 18], fill=col)
        lf = NB(10)
        tx = x + (segw - tw(d, label, lf)) / 2 - 1
        if tx + tw(d, label, lf) > R - 2:
            tx = R - 2 - tw(d, label, lf)
        d.text((tx, by + 4), label, font=lf, fill=WHITE)
        x += segw
    d.text((L, by + 21), "ALL STORIES: FRI 20 NOV 2026, ANY TIME ZONE", font=NB(9), fill=GREY)
    # leads
    ly, lh, lgap = by + 36, 208, 8
    lw = (R - L - 2 * lgap) / 3
    for i, st in enumerate(LEADS):
        lead_card(img, L + i * (lw + lgap), ly, lw, lh, st)
    # grid 5 x 2
    gy = ly + lh + 8
    gh, ggap = 124, 6
    gw = (R - L - 4 * ggap) / 5
    for i, st in enumerate(GRID):
        grid_card(img, L + (i % 5) * (gw + ggap), gy + (i // 5) * (gh + ggap), gw, gh, st)
    # bottom: map + also (2 wide columns, one/two lines per story)
    boty = gy + 2 * gh + ggap + 8
    both = 240
    d.text((L, boty), "WHERE IT HAPPENED", font=NB(11), fill=INK)
    d.text((L + 190, boty + 1), "Pins 1-13 (Lead & Feature)", font=NI(9), fill=GREY)
    pins = [(st["n"], st["pin"][0], st["pin"][1]) for st in LEADS + GRID if st["pin"]]
    draw_map(d, (L, boty + 18, L + 318, boty + 18 + both), pins)
    ax = L + 330
    d.text((ax, boty), "ALSO ON FRIDAY 20 NOVEMBER - 32 MORE STORIES", font=NB(11), fill=INK)
    colw = (R - ax - 14) / 2
    per = 16
    for c in range(2):
        cx = ax + c * (colw + 14)
        cy = boty + 20
        for (n, place, txt) in ALSO[c * per:(c + 1) * per]:
            full = place + " - " + txt
            lines = wrap(d, full, NR(8), colw - 20)
            d.text((cx, cy), str(n), font=NB(8), fill=RED)
            for ln in lines[:2]:
                d.text((cx + 20, cy), ln, font=NR(8), fill=(52, 48, 40))
                cy += 10
            cy += 1
    # date check
    dcy = boty + 18 + both + 10
    d.rectangle([L, dcy, R, dcy + 30], outline=RED, width=2)
    d.text((L + 8, dcy + 4), "DATE CHECK", font=NB(10), fill=RED)
    dl = wrap(d, DATECHECK, NR(9), R - L - 92)
    for j, ln in enumerate(dl[:2]):
        d.text((L + 88, dcy + 4 + j * 12), ln, font=NR(9), fill=(52, 48, 40))
    # footer (single line)
    fy = dcy + 36
    d.line([(L, fy), (R, fy)], fill=RULE, width=1)
    foot = ("Every story here happened, or was first reported, on Friday 20 November 2026 in at least one time zone. "
            "Claims are attributed, not stated as fact. Sources: Reuters, AP, AFP, BBC, IMD, ICC, EU Council, PBOC, UN News, Al Jazeera.")
    d.text((L, fy + 5), foot, font=NI(8), fill=GREY)
    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)

if __name__ == "__main__":
    main()
