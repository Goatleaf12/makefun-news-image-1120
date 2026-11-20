#!/usr/bin/env python3
"""The World in One Day - Friday 20 November 2026 (v2).
One-page newspaper: 50 stories, 7 regions, 13 illustrated.
Deterministic: fixed data, fixed fonts, no randomness, no network."""
from PIL import Image, ImageDraw, ImageFont
import math

SER = "/usr/share/fonts/truetype/liberation/LiberationSerif-%s.ttf"
SAN = "/usr/share/fonts/truetype/liberation/LiberationSans-%s.ttf"

def SF(sz):  return ImageFont.truetype(SER % "Bold", sz)
def SI(sz):  return ImageFont.truetype(SER % "Italic", sz)
def SB(sz):  return ImageFont.truetype(SAN % "Bold", sz)
def NR(sz):  return ImageFont.truetype(SAN % "Regular", sz)
def NB(sz):  return ImageFont.truetype(SAN % "Bold", sz)
def NI(sz):  return ImageFont.truetype(SAN % "Italic", sz)

W, H = 1024, 1024
BG    = (246, 241, 228)
CARD  = (253, 250, 242)
INK   = (26, 24, 20)
RED   = (178, 32, 36)
GREY  = (110, 102, 88)
WHITE = (255, 255, 255)
DARK  = (24, 34, 52)

def tw(d, s, f):
    return d.textlength(s, font=f)

def wrap(d, s, f, maxw):
    out, cur = [], ""
    for word in s.split():
        t = (cur + " " + word).strip()
        if tw(d, t, f) <= maxw or not cur:
            cur = t
        else:
            out.append(cur); cur = word
    if cur:
        out.append(cur)
    return out

def spaced(d, xy, s, f, fill, gap=2):
    x, y = xy
    for ch in s:
        d.text((x, y), ch, font=f, fill=fill)
        x += tw(d, ch, f) + gap
    return x - gap

def fit1(d, s, f, maxw):
    """Force s onto one line, dropping trailing words if needed."""
    while s and tw(d, s, f) > maxw:
        s = s.rsplit(" ", 1)[0]
    return s

def chip(d, xy, s, fill):
    x, y = xy
    w_ = tw(d, s, NB(10)) + 14
    d.rounded_rectangle([x, y, x + w_, y + 17], 4, fill=fill)
    d.text((x + 7, y + 3), s, font=NB(10), fill=WHITE)

# ---------------------------------------------------------------- scenes
def base(w_, h_, top, bot):
    img = Image.new("RGB", (w_, h_), top)
    d = ImageDraw.Draw(img)
    d.rectangle([0, int(h_ * 0.62), w_, h_], fill=bot)
    return img, d

def sc_cyclone(w_, h_):
    img, d = base(w_, h_, (70, 110, 150), (44, 84, 120))
    cx, cy = int(w_ * 0.30), int(h_ * 0.46)
    for r, col in [(46, (225, 232, 238)), (34, (200, 214, 228)), (22, (240, 244, 248))]:
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=col, width=7)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(250, 250, 250))
    for i in range(5):
        x = int(w_ * (0.55 + 0.09 * i))
        d.line([(x, int(h_ * 0.18)), (x - 8, int(h_ * 0.52))], fill=(170, 205, 235), width=3)
    d.polygon([(int(w_ * 0.72), h_), (int(w_ * 0.80), int(h_ * 0.55)),
               (int(w_ * 0.88), h_)], fill=(52, 96, 60))
    d.rectangle([int(w_ * 0.60), int(h_ * 0.80), w_, h_], fill=(214, 196, 150))
    chip(d, (8, 6), "300,000+ EVACUATED", (10, 40, 60))
    return img

def sc_missiles(w_, h_):
    img, d = base(w_, h_, (26, 28, 48), (16, 16, 30))
    for x, y in [(30, 14), (90, 26), (170, 10), (250, 22), (60, 34), (210, 36)]:
        d.ellipse([x, y, x + 3, y + 3], fill=(220, 220, 235))
    for i, bx in enumerate([0.08, 0.30, 0.52, 0.74]):
        x = int(w_ * bx); bh = int(h_ * (0.30 + 0.07 * (i % 3)))
        d.rectangle([x, h_ - bh, x + int(w_ * 0.16), h_], fill=(10, 10, 20))
        for wy in range(h_ - bh + 6, h_ - 6, 9):
            d.rectangle([x + 6, wy, x + 10, wy + 4], fill=(240, 200, 90))
    d.rectangle([int(w_ * 0.40), int(h_ * 0.86), int(w_ * 0.62), h_], fill=(8, 8, 16))
    d.line([(int(w_ * 0.44), int(h_ * 0.86)), (int(w_ * 0.51), int(h_ * 0.60)),
            (int(w_ * 0.58), int(h_ * 0.86))], fill=(8, 8, 16), width=5)
    for sx, sy, ex, ey in [(0.06, 0.06, 0.34, 0.52), (0.22, 0.03, 0.47, 0.50),
                           (0.90, 0.05, 0.63, 0.52), (0.72, 0.02, 0.56, 0.48)]:
        d.line([(int(w_ * sx), int(h_ * sy)), (int(w_ * ex), int(h_ * ey))],
               fill=(255, 176, 84), width=3)
        d.ellipse([int(w_ * ex) - 4, int(h_ * ey) - 4, int(w_ * ex) + 4, int(h_ * ey) + 4],
                  fill=(255, 120, 60))
    chip(d, (8, 6), "~30 MISSILES - 7 WAVES", (52, 14, 14))
    return img

def sc_cop31(w_, h_):
    img, d = base(w_, h_, (196, 168, 110), (150, 128, 82))
    d.rectangle([int(w_ * 0.06), int(h_ * 0.30), int(w_ * 0.94), int(h_ * 0.34)], fill=(90, 70, 40))
    cols = [(200, 60, 50), (60, 110, 180), (240, 190, 60), (70, 150, 80), (150, 80, 160)]
    for i, fx in enumerate([0.10, 0.30, 0.50, 0.70, 0.90]):
        x = int(w_ * fx)
        d.line([(x, int(h_ * 0.32)), (x, int(h_ * 0.62))], fill=(70, 56, 32), width=2)
        d.rectangle([x, int(h_ * 0.36), x + 26, int(h_ * 0.50)], fill=cols[i])
    tx0, ty0, tx1, ty1 = int(w_ * 0.30), int(h_ * 0.66), int(w_ * 0.70), int(h_ * 0.94)
    d.rectangle([tx0, ty0, tx1, ty1], fill=(240, 236, 224))
    d.line([(tx0 + 10, ty0 + 12), (tx1 - 10, ty0 + 12)], fill=(150, 146, 132), width=3)
    d.line([(tx0 + 10, ty0 + 22), (tx1 - 26, ty0 + 22)], fill=(150, 146, 132), width=3)
    d.line([(tx0 + 8, ty1 - 8), (tx1 - 8, ty0 + 6)], fill=RED, width=4)
    chip(d, (8, 6), "FINAL DAY - NO DEAL", (66, 40, 8))
    return img

def sc_selloff(w_, h_):
    img = Image.new("RGB", (w_, h_), (18, 24, 38))
    d = ImageDraw.Draw(img)
    for gx in range(0, w_, 26):
        d.line([(gx, 0), (gx, h_)], fill=(30, 40, 58), width=1)
    for gy in range(0, h_, 18):
        d.line([(0, gy), (w_, gy)], fill=(30, 40, 58), width=1)
    pts = [(0.04, 0.30), (0.22, 0.24), (0.40, 0.38), (0.56, 0.34), (0.72, 0.58), (0.88, 0.52), (0.97, 0.78)]
    xy = [(int(w_ * a), int(h_ * b)) for a, b in pts]
    d.line(xy, fill=(255, 92, 84), width=4)
    for x, y in xy:
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(255, 92, 84))
    d.polygon([(int(w_ * 0.90), int(h_ * 0.66)), (int(w_ * 0.985), int(h_ * 0.80)),
               (int(w_ * 0.90), int(h_ * 0.80))], fill=(255, 92, 84))
    chip(d, (8, 6), "MSCI ASIA -7% WEEK", (70, 16, 16))
    return img

def sc_mercury(w_, h_):
    img = Image.new("RGB", (w_, h_), (8, 10, 22))
    d = ImageDraw.Draw(img)
    for x, y in [(24, 12), (80, 30), (150, 8), (230, 26), (290, 14), (120, 40), (200, 44)]:
        d.ellipse([x, y, x + 3, y + 3], fill=(215, 220, 235))
    cx, cy, r = int(w_ * 0.68), int(h_ * 0.52), int(h_ * 0.34)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(176, 152, 128))
    for ox, oy, orr in [(-0.3, -0.2, 6), (0.2, 0.1, 8), (0.05, -0.45, 4), (-0.1, 0.35, 5)]:
        d.ellipse([cx + int(r * ox) - orr, cy + int(r * oy) - orr,
                   cx + int(r * ox) + orr, cy + int(r * oy) + orr], fill=(150, 126, 102))
    d.arc([int(w_ * 0.06), int(h_ * 0.16), int(w_ * 0.52), int(h_ * 0.92)], 300, 80,
          fill=(120, 170, 220), width=2)
    sx, sy = int(w_ * 0.30), int(h_ * 0.34)
    d.polygon([(sx, sy), (sx + 16, sy + 6), (sx + 4, sy + 14)], fill=(230, 234, 240))
    d.rectangle([sx - 12, sy - 2, sx, sy + 8], fill=(90, 140, 200))
    d.rectangle([sx + 14, sy + 2, sx + 26, sy + 12], fill=(90, 140, 200))
    chip(d, (8, 6), "8 YEARS - 6BN MILES", (14, 30, 52))
    return img

def sc_eudeal(w_, h_):
    img, d = base(w_, h_, (52, 84, 140), (40, 66, 110))
    for i in range(12):
        a = math.radians(i * 30)
        x = int(w_ * 0.24 + 30 * math.cos(a))
        y = int(h_ * 0.46 + 26 * math.sin(a))
        d.polygon([(x, y - 5), (x + 2, y), (x + 5, y), (x, y + 3), (x - 5, y), (x - 2, y)],
                  fill=(250, 205, 60))
    for bx, col in [(0.56, (178, 32, 36)), (0.72, (250, 250, 250))]:
        x = int(w_ * bx)
        d.rectangle([x, int(h_ * 0.24), x + 34, int(h_ * 0.62)], fill=col)
        d.rectangle([x, int(h_ * 0.24), x + 34, int(h_ * 0.36)], fill=(40, 60, 130))
    d.line([(int(w_ * 0.40), int(h_ * 0.46)), (int(w_ * 0.55), int(h_ * 0.46))],
           fill=(250, 205, 60), width=4)
    chip(d, (8, 6), "GBP 5.1BN FOOD DEAL", (16, 34, 62))
    return img

def sc_inflation(w_, h_):
    img = Image.new("RGB", (w_, h_), (240, 234, 218))
    d = ImageDraw.Draw(img)
    for i, bh in enumerate([0.30, 0.38, 0.47, 0.58, 0.72]):
        x = int(w_ * (0.10 + 0.17 * i))
        d.rectangle([x, int(h_ * (0.92 - bh)), x + int(w_ * 0.11), int(h_ * 0.92)],
                    fill=(198, 74, 52) if i == 4 else (120, 130, 150))
    d.line([(int(w_ * 0.06), int(h_ * 0.92)), (int(w_ * 0.96), int(h_ * 0.92))],
           fill=INK, width=2)
    d.polygon([(int(w_ * 0.80), int(h_ * 0.14)), (int(w_ * 0.94), int(h_ * 0.28)),
               (int(w_ * 0.80), int(h_ * 0.28))], fill=RED)
    chip(d, (8, 6), "CPI 2.3% - CORE 2.2%", (90, 30, 20))
    return img

def sc_rates(w_, h_):
    img = Image.new("RGB", (w_, h_), (238, 232, 216))
    d = ImageDraw.Draw(img)
    cx, cy = int(w_ * 0.18), int(h_ * 0.50)
    r = min(22, int(h_ * 0.32))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(150, 40, 40), width=5)
    d.text((cx - 10, cy - 11), "%", font=SB(18), fill=(150, 40, 40))
    for i, (lab, val) in enumerate([("1-YEAR", "3.0%"), ("5-YEAR", "3.5%")]):
        yy = int(h_ * (0.20 + 0.36 * i))
        d.text((int(w_ * 0.40), yy), "%s  %s" % (lab, val), font=SB(13), fill=INK)
    return img

def sc_cricket(w_, h_):
    img, d = base(w_, h_, (96, 150, 84), (74, 128, 64))
    d.rectangle([int(w_ * 0.44), int(h_ * 0.10), int(w_ * 0.56), int(h_ * 0.95)],
                fill=(216, 192, 140))
    for sx in [0.47, 0.50, 0.53]:
        x = int(w_ * sx)
        d.rectangle([x, int(h_ * 0.16), x + 3, int(h_ * 0.30)], fill=(120, 90, 50))
    bx, by = int(w_ * 0.66), int(h_ * 0.42)
    d.line([(bx, by), (bx + 26, by - 18)], fill=(240, 240, 240), width=4)
    d.ellipse([int(w_ * 0.30), int(h_ * 0.30), int(w_ * 0.30) + 9, int(h_ * 0.30) + 9],
              fill=(200, 40, 40))
    chip(d, (8, 6), "PHILLIPS 118 - NZ 368", (26, 58, 26))
    return img

def sc_bukele(w_, h_):
    img, d = base(w_, h_, (70, 96, 150), (54, 76, 122))
    d.rectangle([int(w_ * 0.10), int(h_ * 0.34), int(w_ * 0.90), int(h_ * 0.95)],
                fill=(226, 220, 204))
    for c in range(4):
        x = int(w_ * (0.16 + 0.19 * c))
        d.rectangle([x, int(h_ * 0.44), x + 8, int(h_ * 0.95)], fill=(180, 172, 152))
    d.polygon([(int(w_ * 0.06), int(h_ * 0.34)), (int(w_ * 0.50), int(h_ * 0.16)),
               (int(w_ * 0.94), int(h_ * 0.34))], fill=(120, 60, 50))
    bx, by = int(w_ * 0.50), int(h_ * 0.60)
    d.rectangle([bx - 30, by - 14, bx + 30, by + 14], fill=WHITE, outline=INK, width=2)
    d.rectangle([bx - 30, by - 14, bx + 30, by - 2], fill=(60, 110, 180))
    d.rectangle([bx - 30, by + 2, bx + 30, by + 14], fill=(60, 110, 180))
    chip(d, (8, 6), "THIRD-TERM FILING", (30, 40, 66))
    return img

def sc_boat(w_, h_):
    img, d = base(w_, h_, (216, 178, 120), (38, 84, 118))
    for i in range(3):
        y = int(h_ * (0.66 + 0.11 * i))
        d.arc([int(w_ * 0.04), y - 6, int(w_ * 0.96), y + 10], 0, 180,
              fill=(150, 196, 224), width=3)
    hx, hy = int(w_ * 0.50), int(h_ * 0.58)
    d.polygon([(hx - 52, hy), (hx + 40, hy), (hx + 22, hy + 16), (hx - 34, hy + 16)],
              fill=(120, 62, 34))
    d.line([(hx - 6, hy), (hx - 6, hy - 30)], fill=(80, 50, 30), width=3)
    d.polygon([(hx - 6, hy - 30), (hx - 6, hy - 10), (hx + 16, hy - 12)], fill=(240, 236, 220))
    d.line([(hx - 52, hy + 4), (hx - 78, hy - 14)], fill=(90, 50, 30), width=4)
    chip(d, (8, 6), "4 DEAD - DOZENS MISSING", (70, 30, 16))
    return img

def sc_strike(w_, h_):
    img, d = base(w_, h_, (150, 60, 52), (120, 48, 42))
    for i, fx in enumerate([0.10, 0.30, 0.50, 0.70, 0.88]):
        x = int(w_ * fx)
        d.line([(x, int(h_ * 0.30)), (x, int(h_ * 0.92))], fill=(240, 232, 210), width=3)
        d.rectangle([x - 16, int(h_ * 0.30), x + 16, int(h_ * 0.46)],
                    fill=(240, 236, 224) if i % 2 == 0 else (250, 205, 60))
    for i in range(6):
        x = int(w_ * (0.08 + 0.15 * i)); y = int(h_ * 0.94)
        d.ellipse([x - 5, y - 16, x + 5, y - 6], fill=(30, 26, 24))
        d.rectangle([x - 6, y - 6, x + 6, y + 4], fill=(30, 26, 24))
    chip(d, (8, 6), "24H GENERAL STRIKE", (66, 16, 16))
    return img

def sc_pill(w_, h_):
    img = Image.new("RGB", (w_, h_), (16, 44, 48))
    d = ImageDraw.Draw(img)
    cx, cy = int(w_ * 0.34), int(h_ * 0.52)
    d.rounded_rectangle([cx - 52, cy - 19, cx + 52, cy + 19], 19, fill=(240, 238, 230))
    d.rounded_rectangle([cx, cy - 19, cx + 52, cy + 19], 19, fill=(200, 44, 48))
    d.line([(cx, cy - 19), (cx, cy + 19)], fill=(160, 160, 160), width=2)
    for tx, ty, tr, col in [(int(w_ * 0.76), int(h_ * 0.32), 14, (232, 120, 110)),
                            (int(w_ * 0.86), int(h_ * 0.62), 9, (240, 170, 160)),
                            (int(w_ * 0.68), int(h_ * 0.72), 6, (250, 210, 200))]:
        d.ellipse([tx - tr, ty - tr, tx + tr, ty + tr], outline=col, width=3)
        d.line([(tx - tr + 3, ty), (tx + tr - 3, ty)], fill=col, width=2)
    chip(d, (8, 6), "60.7% RESPONSE", (8, 30, 32))
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
    d.rectangle(box, fill=DARK)
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
    pin_off = {1: (33, 53), 3: (34, 33), 6: (5, 53), 12: (16, 40)}
    for num, lon, lat in pins:
        lon, lat = pin_off.get(num, (lon, lat))
        px, py = proj(lon, lat)
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=WHITE, width=2)
        s = str(num)
        fnt = NB(10 if len(s) < 2 else 9)
        d.text((px - tw(d, s, fnt) / 2, py - 6), s, font=fnt, fill=WHITE)
    d.text((x0 + 8, y1 - 36), "WHERE IT HAPPENED", font=NB(10), fill=(200, 214, 235))
    d.text((x0 + 8, y1 - 18), "SPACE: 5 Mercury - 12 pins on land", font=NB(9), fill=(200, 214, 235))

# ------------------------------------------------------------------ data
# region codes: EU, AP, AM, OC, ME, AF, WO
LEADS = [
    dict(n=1, place="KYIV", beat="UKRAINE", tag="WAR", scene="missiles", reg="EU",
         head="Kyiv hit by ~30 ballistic missiles in seven waves",
         deck="Bridges and districts struck from 01:25 local; casualties reported. Officials, via Reuters."),
    dict(n=2, place="GOPALPUR", beat="INDIA", tag="WEATHER", scene="cyclone", reg="AP",
         head="Cyclone Akvan makes landfall on the Odisha coast",
         deck="300,000+ evacuated; gusts of 90-110 km/h and a storm surge flood the shore. IMD, via PTI."),
    dict(n=3, place="ANTALYA", beat="TURKIYE", tag="CLIMATE", scene="cop31", reg="EU",
         head="COP31 ends its final day deadlocked on fossil fuels",
         deck="The draft omits any phase-out pledge, and a $120bn finance gap stays open. Delegates, via AFP."),
]

GRID = [
    dict(n=4, place="TOKYO", beat="MARKETS", scene="selloff", reg="AP",
         head="Asia's AI sell-off: worst week since 2020",
         deck="Nikkei -4.5%, KOSPI -4.7%, SoftBank -16%; MSCI Asia-Pacific -7%. Reuters."),
    dict(n=5, place="MERCURY", beat="SPACE", scene="mercury", reg="WO",
         head="BepiColombo reaches Mercury after eight years",
         deck="Orbit insertion comes Saturday, after 6bn miles and six flybys. ESA."),
    dict(n=6, place="BRUSSELS", beat="EUROPE", scene="eudeal", reg="EU",
         head="UK and EU sign their reset deal in Brussels",
         deck="A GBP 5.1bn food deal sits at the heart of the package. BBC."),
    dict(n=7, place="TOKYO", beat="ECONOMY", scene="inflation", reg="AP",
         head="Japan inflation holds at 2.3% in October",
         deck="Core CPI 2.2%; a December BoJ hike is eyed. Stats Bureau."),
    dict(n=8, place="BEIJING", beat="ECONOMY", scene="rates", reg="AP",
         head="China holds loan prime rates an 18th month",
         deck="One-year LPR stays 3.0%, five-year 3.5%. PBoC."),
    dict(n=9, place="WELLINGTON", beat="CRICKET", scene="cricket", reg="OC",
         head="Phillips smashes 118 in record NZ total",
         deck="His century lifts the hosts to 368 against India. ICC."),
    dict(n=10, place="SAN SALVADOR", beat="POLITICS", scene="bukele", reg="AM",
         head="Bukele files to run for a third term",
         deck="The vote is set for 28 February 2027. Reports."),
    dict(n=11, place="YENNE", beat="SENEGAL", scene="boat", reg="AF",
         head="Migrant boat capsizes off the Senegal coast",
         deck="Four dead and dozens missing; the search goes on. AFP."),
    dict(n=12, place="TURIN", beat="ITALY", scene="strike", reg="EU",
         head="CGIL calls a 24-hour general strike",
         deck="Rallies fill about 100 squares across Italy. ANSA."),
    dict(n=13, place="BOSTON", beat="HEALTH", scene="pill", reg="AM",
         head="Pancreatic cancer pill beats chemo in trial",
         deck="Daraxonrasib: 60.7% response vs 23-42% on chemo alone. Trial data."),
]

ALSO = [
    (14, "WASHINGTON", "US war cost vs Iran put at $48.3bn - Reuters", "AM"),
    (15, "NEW YORK", "Mamdani plans to close Rikers jail by 2032", "AM"),
    (16, "MEXICO CITY", "116th Revolution Day marked nationwide - AP", "AM"),
    (17, "PORT-AU-PRINCE", "Police raid kills 34 gang suspects - Reuters", "AM"),
    (18, "LAS VEGAS", "Russell fastest in wet GP practice, 1:47.272", "AM"),
    (19, "FLORIDA", "River hits record 18.3 ft; schools shut - AP", "AM"),
    (20, "SAO PAULO", "Markets shut for Black Consciousness Day - AFP", "AM"),
    (21, "LONDON", "UK-Norway fund GBP 100m+ for Ukraine navy - BBC", "EU"),
    (22, "COPENHAGEN", "Greenland defence bill approved - AFP", "EU"),
    (23, "LUBLIN", "Russian missile in Polish field; Tusk protests", "EU"),
    (24, "BERLIN", "Young Germans rally against conscription", "EU"),
    (25, "TURIN", "Alcaraz, Medvedev close ATP Finals groups", "EU"),
    (26, "SMOLENSK", "Drone hit on chemical plant claimed, unverified", "EU"),
    (27, "SEOUL", "Party moves to impeach chief justice - SBS", "AP"),
    (28, "SEOUL", "111 students caught cheating in Suneung exam", "AP"),
    (29, "SHENZHEN", "Xi hails 'full turnaround' with Australia - AAP", "AP"),
    (30, "COX'S BAZAR", "Rohingya pray in camps after ICJ ruling - AJ", "AP"),
    (31, "HORMUZ", "Strait shut; Brent near $92.50, 46 ships wait", "ME"),
    (32, "SAUDI ARABIA", "Coalition 'downs Houthi missile' - a claim", "ME"),
    (33, "BLANTYRE", "Fuel crisis: night queues, 20-litre cap - AJ", "AF"),
    (34, "BOUGAINVILLE", "Rio Tinto pledges $370m for Panguna fleet", "OC"),
    (35, "CANBERRA", "CBO warns AUKUS could shrink US sub fleet", "OC"),
    (36, "TONGA", "Emergency declared amid El Nino drought - RNZ", "OC"),
    (37, "JAKARTA", "Parliament passes asset-forfeiture bill", "AP"),
    (38, "NEW DELHI", "Pakistan minister leads SCO delegation - Hindu", "AP"),
    (39, "HONG KONG", "Badminton Open semi-finals after an upset - BWF", "AP"),
    (40, "KHARKIV", "Drone hits hospital; 4+ hurt - Ukrinform", "EU"),
    (41, "GAZA", "85%+ of civil defence vehicles out of service", "ME"),
    (42, "DAKAR", "Faye enacts extra budget by decree - AFP", "AF"),
    (43, "GLOBAL", "UN marks World Children's Day worldwide", "WO"),
    (44, "CALIFORNIA", "State probes Nvidia over chips in China", "AM"),
    (45, "WELLINGTON", "Nicholls 175* in 216-run stand with Phillips", "OC"),
    (46, "KYIV", "Crews race to restore power after the barrage", "EU"),
    (47, "DHAKA", "Shelters open as Akvan tracks north - officials", "AP"),
    (48, "GENEVA", "WHO notes a rare pancreatic-cancer advance", "EU"),
    (49, "LONDON", "Sterling steady as traders weigh the EU deal", "EU"),
    (50, "TOKYO", "Yen whipsaws on December BoJ hike bets", "AP"),
]

NUMBERS = [
    ("300,000+", "evacuated ahead of Cyclone Akvan"),
    ("~30", "ballistic missiles fired at Kyiv"),
    ("-7%", "Asia shares' worst week since 2020"),
    ("2.3%", "Japan Oct headline CPI; BoJ eyed"),
    ("118", "Phillips' historic century vs India"),
    ("8 yrs", "BepiColombo's journey to Mercury"),
]

REGION_ORDER = [
    ("EU", "EUROPE", (58, 92, 150)),
    ("AP", "ASIA-PACIFIC", (186, 84, 52)),
    ("AM", "AMERICAS", (84, 140, 84)),
    ("OC", "OCEANIA", (110, 84, 140)),
    ("ME", "MIDEAST", (176, 128, 44)),
    ("AF", "AFRICA", (84, 118, 60)),
    ("WO", "WORLD", (60, 60, 70)),
]

PINS = [(1, 30, 50), (2, 85, 19), (3, 31, 37), (4, 128, 31), (6, 0, 51),
        (7, 139, 36), (8, 116, 40), (9, 175, -41), (10, -89, 14),
        (11, -17, 15), (12, 8, 45), (13, -71, 42)]

DATECHECK = ("First reported Thursday 19 Nov, so NOT shown as Friday's news: the Trump-Xi-Putin "
             "Shenzhen summit itself - Anthropic's $83 IPO pricing and Nasdaq debut - the ICJ's Myanmar "
             "Rohingya genocide verdict - GTA VI's midnight launch - Voyager 1's one light-day "
             "confirmation - the Senate's 48-51 Iran war-powers vote - Fiona the hippo's death.")

# ---------------------------------------------------------------- layout
L, R = 22, 1002
CW = R - L

def lead_card(img, x, y, w_, st):
    x, y, w_ = int(x), int(y), int(w_)
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w_, y + 218], fill=CARD, outline=(190, 180, 156), width=1)
    img.paste(SCENES[st["scene"]](w_ - 16, 96), (x + 8, y + 8))
    cy = y + 109
    kick = "%02d - %s - %s" % (st["n"], st["place"], st["beat"])
    d.text((x + 10, cy), kick, font=NB(10), fill=RED)
    tagw = tw(d, st["tag"], NI(10))
    d.text((x + w_ - 10 - tagw, cy), st["tag"], font=NI(10), fill=GREY)
    cy += 15
    for ln in wrap(d, st["head"], SB(20), w_ - 20)[:2]:
        d.text((x + 10, cy), ln, font=SB(20), fill=INK)
        cy += 23
    cy += 3
    for ln in wrap(d, st["deck"], NR(12), w_ - 20)[:3]:
        d.text((x + 10, cy), ln, font=NR(12), fill=(52, 48, 40))
        cy += 15

def grid_card(img, x, y, w_, st):
    x, y, w_ = int(x), int(y), int(w_)
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w_, y + 138], fill=CARD, outline=(190, 180, 156), width=1)
    img.paste(SCENES[st["scene"]](w_ - 12, 50), (x + 6, y + 6))
    cy = y + 60
    kick = "%02d - %s - %s" % (st["n"], st["place"], st["beat"])
    d.text((x + 8, cy), fit1(d, kick, NB(9), w_ - 16), font=NB(9), fill=RED)
    cy += 12
    for ln in wrap(d, st["head"], SB(14), w_ - 16)[:2]:
        d.text((x + 8, cy), ln, font=SB(14), fill=INK)
        cy += 17
    cy += 2
    for ln in wrap(d, st["deck"], NR(10), w_ - 16)[:2]:
        d.text((x + 8, cy), ln, font=NR(10), fill=(52, 48, 40))
        cy += 13

def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # masthead
    spaced(d, (L, 10), "THE WORLD IN ONE DAY", NB(12), RED, gap=2)
    rtxt = "ONE PAGE - 50 STORIES - 7 REGIONS"
    d.text((R - tw(d, rtxt, NB(11)), 11), rtxt, font=NB(11), fill=GREY)
    d.text((L, 28), "FRIDAY 20 NOVEMBER 2026", font=SF(42), fill=INK)
    sub = ("Cyclone Akvan ashore in Odisha - a ballistic barrage over Kyiv - "
           "COP31 deadlocked - and a visitor reaches Mercury")
    d.text((L, 80), fit1(d, sub, SI(16), CW), font=SI(16), fill=(70, 62, 48))
    d.rectangle([L, 103, R, 106], fill=INK)
    d.line([(L, 109), (R, 109)], fill=INK, width=1)
    # the day in numbers
    y = 116
    spaced(d, (L, y), "THE DAY IN NUMBERS", NB(10), RED, gap=1)
    y += 14
    cellw = CW / 6
    for i, (num, cap) in enumerate(NUMBERS):
        x = L + i * cellw
        d.text((x, y), num, font=SF(24), fill=RED if num == "-7%" else INK)
        for j, ln in enumerate(wrap(d, cap, NB(8), cellw - 10)[:2]):
            d.text((x, y + 29 + j * 10), ln, font=NB(8), fill=GREY)
    y += 48
    d.line([(L, y), (R, y)], fill=(190, 180, 156), width=1)
    y += 5
    # region bar (counts computed from the story data itself)
    counts = {}
    for st in LEADS + GRID:
        counts[st["reg"]] = counts.get(st["reg"], 0) + 1
    for _, _, _, reg in ALSO:
        counts[reg] = counts.get(reg, 0) + 1
    total = sum(counts.values())
    assert total == 50, total
    x = L
    for code, label, col in REGION_ORDER:
        segw = CW * counts[code] / total
        d.rectangle([x, y, x + segw - 2, y + 20], fill=col)
        lab = "%s %d" % (label, counts[code])
        if tw(d, lab, NB(9)) <= segw - 8:
            d.text((x + (segw - 2 - tw(d, lab, NB(9))) / 2, y + 5), lab, font=NB(9), fill=WHITE)
        else:
            s = str(counts[code])
            d.text((x + (segw - 2 - tw(d, s, NB(9))) / 2, y + 5), s, font=NB(9), fill=WHITE)
        x += segw
    y += 24
    # leads
    lw = (CW - 26) / 3
    for i, st in enumerate(LEADS):
        lead_card(img, L + i * (lw + 13), y, lw, st)
    y += 220
    # grid
    gw = (CW - 40) / 5
    for r_ in range(2):
        for c_ in range(5):
            grid_card(img, L + c_ * (gw + 10), y + r_ * 142, gw, GRID[r_ * 5 + c_])
    y += 284
    # map
    draw_map(d, [L, y, R, y + 76], PINS)
    y += 82
    # also
    d.text((L, y), "ALSO FRIDAY", font=SB(14), fill=RED)
    d.text((L + tw(d, "ALSO FRIDAY", SB(14)) + 8, y + 2),
           "- 37 more stories from the wires", font=NR(11), fill=INK)
    y += 18
    d.line([(L, y), (R, y)], fill=(190, 180, 156), width=1)
    y += 3
    colw = (CW - 26) / 3
    cols = [ALSO[0:13], ALSO[13:26], ALSO[26:37]]
    for ci, col in enumerate(cols):
        cx = L + ci * (colw + 13)
        cyy = y
        for n, place, text, _ in col:
            head = "%02d %s - " % (n, place)
            hw = tw(d, head, NB(10))
            d.text((cx, cyy), head, font=NB(10), fill=INK)
            d.text((cx + hw, cyy), fit1(d, text, NR(10), colw - hw), font=NR(10),
                   fill=(52, 48, 40))
            cyy += 12
    y += 13 * 12 + 3
    # date check
    d.rectangle([L, y, R, y + 27], outline=RED, width=2)
    d.text((L + 8, y + 4), "DATE CHECK", font=NB(10), fill=RED)
    dx = L + 8 + tw(d, "DATE CHECK", NB(10)) + 8
    lines = wrap(d, DATECHECK, NR(9), R - dx - 8)
    d.text((dx, y + 4), lines[0], font=NR(9), fill=INK)
    for j, ln in enumerate(wrap(d, " ".join(lines[1:]), NR(9), CW - 16)[:1]):
        d.text((L + 8, y + 16), ln, font=NR(9), fill=INK)
    y += 30
    # footer
    d.line([(L, y), (R, y)], fill=INK, width=2)
    foot = "Every story here happened, or was first reported, on Friday 20 November 2026."
    d.text(((W - tw(d, foot, NB(10))) / 2, y + 5), foot, font=NB(10), fill=INK)
    assert y + 20 <= H, y
    img.save("entry.png")
    print("wrote entry.png, bottom =", y + 20)

if __name__ == "__main__":
    main()
