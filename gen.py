#!/usr/bin/env python3
"""The World in One Day - Friday 20 November 2026 (v3).
One-page newspaper in the classic broadsheet system: serif display
headlines, prose decks with attributed sources, labelled scenes,
a dark map beside the wire briefs. 50 stories, 7 regions, 13 drawn.
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
    while s and tw(d, s, f) > maxw:
        s = s.rsplit(" ", 1)[0]
    return s

def chip(d, xy, s, fill):
    x, y = xy
    w_ = tw(d, s, NB(10)) + 14
    d.rounded_rectangle([x, y, x + w_, y + 17], 4, fill=fill)
    d.text((x + 7, y + 3), s, font=NB(10), fill=WHITE)

def band(d, w_, h_, left, right=None):
    """Dark label band across the bottom of a lead scene."""
    d.rectangle([0, h_ - 20, w_, h_], fill=(16, 18, 26))
    d.text((8, h_ - 15), left, font=NB(10), fill=WHITE)
    if right:
        d.text((w_ - 8 - tw(d, right, NB(9)), h_ - 14), right, font=NB(9),
               fill=(250, 205, 60))

# ---------------------------------------------------------------- scenes
def base(w_, h_, top, bot):
    img = Image.new("RGB", (w_, h_), top)
    d = ImageDraw.Draw(img)
    d.rectangle([0, int(h_ * 0.62), w_, h_], fill=bot)
    return img, d

def sc_cyclone(w_, h_):
    img, d = base(w_, h_, (70, 110, 150), (44, 84, 120))
    # coast of Odisha on the left, Bay of Bengal to the right
    d.polygon([(0, 0), (int(w_ * 0.30), 0), (int(w_ * 0.24), int(h_ * 0.38)),
               (int(w_ * 0.34), int(h_ * 0.66)), (int(w_ * 0.28), h_), (0, h_)],
              fill=(214, 196, 150))
    d.text((10, 10), "ODISHA", font=NB(10), fill=(90, 74, 40))
    d.text((10, 24), "INDIA", font=NB(9), fill=(90, 74, 40))
    d.text((12, int(h_ * 0.52)), "Gopalpur", font=NI(10), fill=(70, 58, 32))
    gx, gy = int(w_ * 0.26), int(h_ * 0.60)
    d.ellipse([gx - 4, gy - 4, gx + 4, gy + 4], fill=RED)
    cx, cy = int(w_ * 0.62), int(h_ * 0.40)
    for r, col in [(52, (225, 232, 238)), (39, (200, 214, 228)), (25, (240, 244, 248))]:
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 305, fill=col, width=8)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(250, 250, 250))
    d.text((int(w_ * 0.58), int(h_ * 0.74)), "BAY OF BENGAL", font=NB(10),
           fill=(190, 216, 238))
    for i in range(5):
        x = int(w_ * (0.80 + 0.045 * i))
        d.line([(x, int(h_ * 0.10)), (x - 7, int(h_ * 0.34))], fill=(170, 205, 235), width=3)
    band(d, w_, h_, "LANDFALL - GUSTS 110 KM/H", "CYCLONE AKVAN")
    return img

def sc_missiles(w_, h_):
    img, d = base(w_, h_, (26, 28, 48), (16, 16, 30))
    for x, y in [(30, 14), (90, 26), (170, 10), (250, 22), (60, 34), (210, 36), (130, 20)]:
        d.ellipse([x, y, x + 3, y + 3], fill=(220, 220, 235))
    d.ellipse([int(w_ * 0.86), int(h_ * 0.10), int(w_ * 0.86) + 16, int(h_ * 0.10) + 16],
              fill=(232, 228, 205))
    d.ellipse([int(w_ * 0.86) + 5, int(h_ * 0.10) + 2, int(w_ * 0.86) + 19, int(h_ * 0.10) + 14],
              fill=(26, 28, 48))
    for i, bx in enumerate([0.06, 0.26, 0.46, 0.66]):
        x = int(w_ * bx); bh = int(h_ * (0.34 + 0.08 * (i % 3)))
        d.rectangle([x, h_ - 20 - bh, x + int(w_ * 0.15), h_ - 20], fill=(10, 10, 20))
        for wy in range(h_ - 20 - bh + 6, h_ - 28, 10):
            for wx in range(x + 5, x + int(w_ * 0.15) - 6, 11):
                d.rectangle([wx, wy, wx + 4, wy + 4], fill=(240, 200, 90))
    d.rectangle([int(w_ * 0.38), int(h_ * 0.80), int(w_ * 0.60), h_ - 20], fill=(8, 8, 16))
    d.line([(int(w_ * 0.42), int(h_ * 0.80)), (int(w_ * 0.49), int(h_ * 0.56)),
            (int(w_ * 0.56), int(h_ * 0.80))], fill=(8, 8, 16), width=5)
    for sx, sy, ex, ey in [(0.05, 0.05, 0.33, 0.52), (0.20, 0.02, 0.46, 0.50),
                           (0.92, 0.22, 0.64, 0.54), (0.74, 0.03, 0.57, 0.48),
                           (0.38, 0.02, 0.50, 0.46)]:
        d.line([(int(w_ * sx), int(h_ * sy)), (int(w_ * ex), int(h_ * ey))],
               fill=(255, 176, 84), width=3)
        d.ellipse([int(w_ * ex) - 4, int(h_ * ey) - 4, int(w_ * ex) + 4, int(h_ * ey) + 4],
                  fill=(255, 120, 60))
    band(d, w_, h_, "01:25 LOCAL - 7 WAVES", "~30 MISSILES")
    return img

def sc_cop31(w_, h_):
    img, d = base(w_, h_, (196, 168, 110), (150, 128, 82))
    # thermometer, left
    tx = int(w_ * 0.16)
    d.rectangle([tx - 6, int(h_ * 0.14), tx + 6, int(h_ * 0.66)], fill=(240, 238, 230),
                outline=(90, 70, 40), width=2)
    d.rectangle([tx - 4, int(h_ * 0.30), tx + 4, int(h_ * 0.66)], fill=RED)
    d.ellipse([tx - 13, int(h_ * 0.60), tx + 13, int(h_ * 0.60) + 26], fill=RED)
    for i in range(4):
        yy = int(h_ * (0.20 + 0.11 * i))
        d.line([(tx + 8, yy), (tx + 14, yy)], fill=(90, 70, 40), width=2)
    # flags row, centre
    cols = [(200, 60, 50), (60, 110, 180), (240, 190, 60), (70, 150, 80)]
    for i, fx in enumerate([0.36, 0.46, 0.56, 0.66]):
        x = int(w_ * fx)
        d.line([(x, int(h_ * 0.16)), (x, int(h_ * 0.52))], fill=(70, 56, 32), width=2)
        d.rectangle([x, int(h_ * 0.18), x + 22, int(h_ * 0.31)], fill=cols[i])
    # the summit sign, right
    sx0, sy0, sx1, sy1 = int(w_ * 0.66), int(h_ * 0.12), int(w_ * 0.98), int(h_ * 0.62)
    d.rectangle([sx0, sy0, sx1, sy1], fill=(250, 248, 240), outline=(90, 70, 40), width=2)
    d.rectangle([sx0, sy0, sx1, sy0 + 15], fill=RED)
    d.text((sx0 + 6, sy0 + 3), "ANTALYA - NOV 20", font=NB(9), fill=WHITE)
    d.text((sx0 + 6, sy0 + 19), "COP31", font=SF(21), fill=INK)
    d.text((sx0 + 6, sy1 - 13), "FINAL DAY - DEADLOCK", font=NB(8), fill=RED)
    band(d, w_, h_, "UN CLIMATE SUMMIT", "$120BN FINANCE GAP")
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
    chip(d, (8, 6), "ASIA -7% WK", (70, 16, 16))
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
    chip(d, (8, 6), "6BN MILES", (14, 30, 52))
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
    chip(d, (8, 6), "RESET TALKS", (16, 34, 62))
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
    chip(d, (8, 6), "CPI 2.3%", (90, 30, 20))
    return img

def sc_rates(w_, h_):
    img = Image.new("RGB", (w_, h_), (238, 232, 216))
    d = ImageDraw.Draw(img)
    d.rectangle([int(w_ * 0.06), int(h_ * 0.16), int(w_ * 0.94), int(h_ * 0.40)],
                fill=(52, 44, 30))
    d.text((int(w_ * 0.10), int(h_ * 0.22)), "18 MO UNCHANGED", font=NB(10), fill=WHITE)
    for i, (lab, val) in enumerate([("3.50% 5Y", 0.62), ("3.00% 1Y", 0.44)]):
        yy = int(h_ * (0.52 + 0.24 * i))
        d.rectangle([int(w_ * 0.08), yy, int(w_ * val), yy + 9], fill=RED if i == 0 else (120, 130, 150))
        d.text((int(w_ * val) + 6, yy - 2), lab, font=NB(11), fill=INK)
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
    chip(d, (8, 6), "118 - RECORD", (26, 58, 26))
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
    d.rectangle([int(w_ * 0.40), int(h_ * 0.52), int(w_ * 0.60), int(h_ * 0.78)],
                fill=(24, 34, 52))
    d.text((int(w_ * 0.435), int(h_ * 0.585)), "2027", font=SF(15), fill=(250, 205, 60))
    chip(d, (8, 6), "THIRD TERM", (30, 40, 66))
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
    chip(d, (8, 6), "YENNE COAST", (70, 30, 16))
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
    chip(d, (8, 6), "SCIOPERO - 100 SQUARES", (66, 16, 16))
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
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=WHITE, width=2)
        s = str(num)
        fnt = NB(9 if len(s) < 2 else 8)
        d.text((px - tw(d, s, fnt) / 2, py - 5), s, font=fnt, fill=WHITE)
    d.ellipse([x0 + 10, y1 - 40, x0 + 22, y1 - 28], fill=RED, outline=WHITE, width=1)
    d.text((x0 + 26, y1 - 39), "5 SPACE", font=NB(8), fill=(200, 214, 235))
    d.text((x0 + 26, y1 - 28), "Mercury", font=NB(8), fill=(200, 214, 235))
    lx = x0 + 120
    d.ellipse([lx, y1 - 26, lx + 9, y1 - 17], fill=RED)
    d.text((lx + 13, y1 - 26), "1-3 Lead", font=NB(8), fill=(200, 214, 235))
    d.ellipse([lx + 76, y1 - 26, lx + 85, y1 - 17], fill=RED)
    d.text((lx + 89, y1 - 26), "4-13 Feature", font=NB(8), fill=(200, 214, 235))

# ------------------------------------------------------------------ data
# region codes: EU, AP, AM, OC, ME, AF, WO
LEADS = [
    dict(n=1, place="KYIV, UKRAINE", beat="WAR", scene="missiles", reg="EU",
         head="Russia fires wave of ~30 ballistic missiles at Kyiv",
         deck="Seven overnight waves hit energy and transport sites; fires burn in three "
              "districts; Dutch and Austrian embassies damaged. (Kyiv Post, Reuters)"),
    dict(n=2, place="ODISHA, INDIA", beat="CYCLONE", scene="cyclone", reg="AP",
         head="Cyclone Akvan makes landfall in eastern India",
         deck="Severe storm crosses near Gopalpur; 300,000+ evacuated, winds 90-100 "
              "gusting 110 km/h; 423 rescue teams deployed, schools shut. (IMD, The Hindu)"),
    dict(n=3, place="ANTALYA, TURKIYE", beat="CLIMATE", scene="cop31", reg="EU",
         head="COP31 reaches its final day deadlocked",
         deck="Closing draft omits fossil-fuel phase-out while $120bn adaptation finance "
              "stays unresolved; hosts push a '35 by 35' clean-power goal. (UN News, Reuters)"),
]

GRID = [
    dict(n=4, place="SEOUL/TOKYO", beat="MARKETS", scene="selloff", reg="AP",
         head="AI sell-off sinks Asia to worst week since 2020",
         deck="Nikkei -4.5%, KOSPI -4.7%, SoftBank -16%; MSCI Asia down 7%. (Reuters)"),
    dict(n=5, place="MERCURY", beat="SPACE", scene="mercury", reg="WO",
         head="BepiColombo reaches Mercury after 8 years",
         deck="ESA/JAXA probe ends 6bn-mile trip; insertion Saturday. (ESA)"),
    dict(n=6, place="BRUSSELS", beat="EUROPE", scene="eudeal", reg="EU",
         head="Burnham holds first EU-UK reset summit",
         deck="Brussels hosts UK PM; agrifood, carbon links eyed. (EU Council)"),
    dict(n=7, place="TOKYO", beat="ECONOMY", scene="inflation", reg="AP",
         head="Japan inflation hits 2.3%; BoJ hike eyed",
         deck="Oct CPI rises from 2.1%; core above 2% for second month. (Reuters)"),
    dict(n=8, place="BEIJING", beat="RATES", scene="rates", reg="AP",
         head="China holds lending rates for 18th month",
         deck="1-year LPR stays at 3.0%, 5-year at 3.5% as expected. (PBOC)"),
    dict(n=9, place="WELLINGTON", beat="CRICKET", scene="cricket", reg="OC",
         head="Phillips makes history with 118 vs India",
         deck="First NZ batter with 3-format centuries in a year; 368. (ICC)"),
    dict(n=10, place="SAN SALVADOR", beat="POLITICS", scene="bukele", reg="AM",
         head="Bukele registers for third-term run",
         deck="Files for Feb 2027 vote; rights groups object. (AP)"),
    dict(n=11, place="SENEGAL", beat="MIGRATION", scene="boat", reg="AF",
         head="Migrant boat capsizes off Yenne: 4 dead",
         deck="Dozens missing from ~50-100 aboard; Canary surge. (Al Jazeera)"),
    dict(n=12, place="ROME", beat="LABOUR", scene="strike", reg="EU",
         head="Italy's CGIL holds 24-hr general strike",
         deck="Unions rally in ~100 squares against 2027 budget. (CGIL, AFP)"),
    dict(n=13, place="BARCELONA", beat="HEALTH", scene="pill", reg="AM",
         head="Pancreatic cancer pill shrinks tumours 60.7%",
         deck="Daraxonrasib + chemo beats chemo alone (23-42%). (Reuters)"),
]

# (n, dateline, brief, source, region)
ALSO = [
    (14, "WASHINGTON", "Pentagon puts US war cost against Iran at $48.3bn", "Reuters", "AM"),
    (15, "NEW YORK", "Mamdani plans to close Rikers Island jail by 2032", "reports", "AM"),
    (16, "MEXICO CITY", "Nation marks its 116th Revolution Day", "AP", "AM"),
    (17, "PORT-AU-PRINCE", "Forces kill 34 gang suspects in raid", "Reuters", "AM"),
    (18, "LAS VEGAS", "Russell fastest in wet GP practice, 1:47.272", "F1", "AM"),
    (19, "FLORIDA", "St Johns River hits record 18.3 ft; schools shut", "AP", "AM"),
    (20, "SAO PAULO", "Markets shut for Black Consciousness Day", "AFP", "AM"),
    (21, "LONDON", "UK & Norway fund 100m+ for two Ukrainian naval vessels", "BBC", "EU"),
    (22, "COPENHAGEN", "Parliament approves Greenland defence bill", "AFP", "EU"),
    (23, "WARSAW", "Poland probes objects downed in the strikes", "Reuters", "EU"),
    (24, "BERLIN", "Ukraine's allies meet; Europe 'ready to talk'", "BBC", "EU"),
    (25, "TURIN", "Alcaraz-Cobolli, Medvedev-Tiafoe close ATP groups", "ATP", "EU"),
    (26, "SMOLENSK", "Drone strike reported on chemical plant", "Kyiv Indep.", "EU"),
    (27, "SEOUL", "Ruling party moves to impeach Chief Justice Cho", "SBS", "AP"),
    (28, "SEOUL", "111 students caught cheating in Suneung exam", "officials", "AP"),
    (29, "SHENZHEN", "Xi hails a 'full turnaround' with Australia", "CGTN, AAP", "AP"),
    (30, "COX'S BAZAR", "Rohingya pray in camps after the ICJ ruling", "Al Jazeera", "AP"),
    (31, "HORMUZ", "Four attacks on vessels in 96 hours, centre says", "UKMTO", "ME"),
    (32, "RIYADH", "Houthi missiles damage PIF tower; Gulf condemns", "Sky", "ME"),
    (33, "BLANTYRE", "Fuel crisis: night queues, 20-litre daily cap", "Al Jazeera", "AF"),
    (34, "BOUGAINVILLE", "Rio Tinto pledges $370m for Panguna mine fleet", "Reuters", "OC"),
    (35, "CANBERRA", "CBO warns AUKUS sub sales could shrink US fleet", "Reuters", "OC"),
    (36, "TONGA", "Kingdom declares emergency as El Nino drought bites", "RNZ", "OC"),
    (37, "JAKARTA", "Parliament passes asset-forfeiture bill", "Reuters", "AP"),
    (38, "NEW DELHI", "Pakistan minister to lead delegation to SCO dialogue", "Hindu", "AP"),
    (39, "HONG KONG", "Badminton Open reaches semis after upset", "BWF", "AP"),
    (40, "KHARKIV", "Drone hits a hospital; at least four hurt", "Ukrinform", "EU"),
    (41, "GAZA", "Israeli troops cross Yellow Line; Hamas cries foul", "UPI", "ME"),
    (42, "DAKAR", "President Faye enacts supplementary budget by decree", "AFP", "AF"),
    (43, "GLOBAL", "UN marks World Children's Day across member states", "UN News", "WO"),
    (44, "CALIFORNIA", "Attorney general subpoenas Nvidia in chips probe", "CNBC", "AM"),
    (45, "WELLINGTON", "Henry Nicholls scores 175* in 216-run stand", "ICC", "OC"),
    (46, "KYIV", "Crews race to restore power and heat citywide", "officials", "EU"),
    (47, "DHAKA", "Shelters open as Akvan's bands lash the coast", "officials", "AP"),
    (48, "GENEVA", "WHO notes a rare pancreatic-cancer advance", "reported", "EU"),
    (49, "LONDON", "Sterling steady as traders weigh the reset deal", "markets", "EU"),
    (50, "TOKYO", "Yen whipsaws as December BoJ hike bets build", "markets", "AP"),
]

NUMBERS = [
    ("300,000+", "evacuated ahead of Cyclone Akvan", False),
    ("~30", "ballistic missiles fired at Kyiv", False),
    ("-7%", "Asia shares' worst week since 2020", True),
    ("2.3%", "Japan Oct headline CPI; BoJ eyed", True),
    ("118", "Phillips' historic century vs India", False),
    ("8 yrs", "BepiColombo reaches Mercury", False),
]

REGION_ORDER = [
    ("EU", "EUROPE", (58, 92, 150)),
    ("AP", "ASIA-PACIFIC", (186, 84, 52)),
    ("AM", "AMERICAS", (84, 140, 84)),
    ("OC", "OCEANIA", (110, 84, 140)),
    ("ME", "MIDEAST", (176, 128, 44)),
    ("AF", "AFRICA", (84, 118, 60)),
    ("WO", "WORLD / SPACE", (60, 60, 70)),
]

PINS = [(1, 30, 50), (2, 85, 19), (3, 31, 37), (4, 128, 31), (6, 0, 51),
        (7, 139, 36), (8, 116, 40), (9, 175, -41), (10, -89, 14),
        (11, -17, 15), (12, 12.5, 42), (13, 2, 41)]

DATECHECK = ("First reported Thursday 19 Nov, so NOT shown as Friday's news: the Trump-Xi-Putin "
             "Shenzhen summit itself - Anthropic's $83 IPO pricing & Nasdaq debut - the ICJ Myanmar "
             "Rohingya genocide verdict - GTA VI midnight launch - Voyager 1 one light-day "
             "confirmation - Senate 48-51 Iran war-powers vote - Fiona the hippo's death.")

# ---------------------------------------------------------------- layout
L, R = 22, 1002
CW = R - L

def lead_card(img, x, y, w_, st):
    x, y, w_ = int(x), int(y), int(w_)
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w_, y + 250], fill=CARD, outline=(190, 180, 156), width=1)
    img.paste(SCENES[st["scene"]](w_ - 16, 118), (x + 8, y + 8))
    cy = y + 132
    kick = "%02d - %s - %s" % (st["n"], st["place"], st["beat"])
    d.text((x + 10, cy), kick, font=NB(10), fill=RED)
    cy += 16
    for ln in wrap(d, st["head"], SF(23), w_ - 20)[:2]:
        d.text((x + 10, cy), ln, font=SF(23), fill=INK)
        cy += 27
    cy += 3
    for ln in wrap(d, st["deck"], NR(11), w_ - 20)[:3]:
        d.text((x + 10, cy), ln, font=NR(11), fill=(52, 48, 40))
        cy += 15

def grid_card(img, x, y, w_, st):
    x, y, w_ = int(x), int(y), int(w_)
    d = ImageDraw.Draw(img)
    d.rectangle([x, y, x + w_, y + 138], fill=CARD, outline=(190, 180, 156), width=1)
    img.paste(SCENES[st["scene"]](w_ - 12, 50), (x + 6, y + 6))
    cy = y + 60
    kick = "%02d - %s - %s" % (st["n"], st["place"], st["beat"])
    d.text((x + 8, cy), fit1(d, kick, NB(9), w_ - 16), font=NB(9), fill=RED)
    cy += 13
    for ln in wrap(d, st["head"], SF(14), w_ - 16)[:2]:
        d.text((x + 8, cy), ln, font=SF(14), fill=INK)
        cy += 17
    cy += 2
    for ln in wrap(d, st["deck"], NR(10), w_ - 16)[:2]:
        d.text((x + 8, cy), ln, font=NR(10), fill=(52, 48, 40))
        cy += 12

def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # masthead
    spaced(d, (L, 8), "THE WORLD IN ONE DAY", NB(11), RED, gap=2)
    rtxt = "FRIDAY'S NEWS - ONE PAGE - 50 STORIES - 7 REGIONS"
    d.text((R - tw(d, rtxt, NB(10)), 9), rtxt, font=NB(10), fill=GREY)
    d.text((L, 24), "Friday 20 November 2026", font=SF(54), fill=INK)
    sub = ("Cyclone Akvan strikes India - Ballistic missiles hit Kyiv - "
           "COP31 deadlocked on final day - Asian AI sell-off")
    d.text((L, 84), fit1(d, sub, SI(15), CW), font=SI(15), fill=(150, 44, 40))
    d.rectangle([L, 103, R, 106], fill=INK)
    d.line([(L, 109), (R, 109)], fill=INK, width=1)
    # the day in numbers
    y = 114
    cellw = CW / 6
    for i, (num, cap, isred) in enumerate(NUMBERS):
        x = L + i * cellw
        if i > 0:
            d.line([(x, y + 2), (x, y + 48)], fill=(190, 180, 156), width=1)
        d.text((x + 8, y), num, font=SF(25), fill=RED if isred else INK)
        for j, ln in enumerate(wrap(d, cap, NB(8), cellw - 14)[:2]):
            d.text((x + 8, y + 30 + j * 10), ln, font=NB(8), fill=GREY)
    y += 56
    # region bar (counts computed from the story data itself)
    counts = {}
    for st in LEADS + GRID:
        counts[st["reg"]] = counts.get(st["reg"], 0) + 1
    for _, _, _, _, reg in ALSO:
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
    y += 28
    # leads
    lw = (CW - 26) / 3
    for i, st in enumerate(LEADS):
        lead_card(img, L + i * (lw + 13), y, lw, st)
    y += 256
    # grid
    gw = (CW - 40) / 5
    for r_ in range(2):
        for c_ in range(5):
            grid_card(img, L + c_ * (gw + 10), y + r_ * 144, gw, GRID[r_ * 5 + c_])
    y += 288
    # bottom: map left, also right
    d.text((L, y), "WHERE IT HAPPENED", font=SB(12), fill=INK)
    ax = L + 364
    d.text((ax, y), "ALSO ON FRIDAY 20 NOVEMBER - 37 MORE STORIES", font=SB(12), fill=INK)
    wb = "World Briefs (14-50)"
    d.text((R - tw(d, wb, NI(10)), y + 1), wb, font=NI(10), fill=GREY)
    y += 18
    draw_map(d, [L, y, L + 350, y + 208], PINS)
    colw = (R - ax - 16) / 2
    cols = [ALSO[0:19], ALSO[19:37]]
    for ci, col in enumerate(cols):
        cx = ax + ci * (colw + 16)
        cyy = float(y)
        for n, place, text, src, _ in col:
            num = "%02d " % n
            d.text((cx, int(cyy)), num, font=NB(9), fill=RED)
            x2 = cx + tw(d, num, NB(9))
            pl = place + " "
            d.text((x2, int(cyy)), pl, font=NB(9), fill=INK)
            x3 = x2 + tw(d, pl, NB(9))
            tail = " (%s)" % src
            avail = colw - (x3 - cx) - tw(d, tail, NI(9))
            d.text((x3, int(cyy)), fit1(d, text, NR(9), avail), font=NR(9), fill=(52, 48, 40))
            d.text((x3 + tw(d, fit1(d, text, NR(9), avail), NR(9)), int(cyy)), tail,
                   font=NI(9), fill=GREY)
            cyy += 11
    y += 216
    # date check
    d.rectangle([L, y, R, y + 24], outline=RED, width=2)
    d.text((L + 8, y + 6), "DATE CHECK", font=NB(10), fill=RED)
    dx = L + 8 + tw(d, "DATE CHECK", NB(10)) + 8
    lines = wrap(d, DATECHECK, NR(9), R - dx - 8)
    d.text((dx, y + 3), lines[0], font=NR(9), fill=INK)
    rest = " ".join(lines[1:])
    d.text((L + 8, y + 14), fit1(d, rest, NR(9), CW - 16), font=NR(9), fill=INK)
    y += 30
    # footer
    d.line([(L, y), (R, y)], fill=INK, width=2)
    foot = "Every story here happened, or was first reported, on Friday 20 November 2026."
    d.text((L, y + 4), foot, font=NB(9), fill=INK)
    src = "Sources: Reuters, AP, AFP, BBC, IMD, UN News, Al Jazeera, ICC, EU Council, PBOC"
    d.text((R - tw(d, src, NI(8)), y + 5), src, font=NI(8), fill=GREY)
    assert y + 16 <= H, y
    img.save("entry.png")
    print("wrote entry.png, bottom =", y + 16)

if __name__ == "__main__":
    main()
