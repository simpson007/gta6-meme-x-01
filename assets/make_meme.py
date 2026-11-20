#!/usr/bin/env python3
"""Build meme.png for the gta6-meme-x-01 bounty.

Scene: a Vice City sunset. The make.fun ghost (the agent) stands in front of
the sun, waiting. The joke: 13 years waiting for GTA 6, while the agent is
already earning on make.fun. Everything is drawn with PIL; the ghost is the
official press-kit mark (assets/mark-1024.png), composited large in the
middle of the scene, not a corner sticker.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1080
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
GHOST = "assets/mark-1024.png"
OUT = "meme.png"

random.seed(20261120)

# ---------- sunset gradient ----------
stops = [(0.0, (26, 11, 46)), (0.45, (146, 27, 84)), (0.75, (255, 46, 136)), (1.0, (255, 140, 66))]
img = Image.new("RGB", (W, H))
px = img.load()
for y in range(H):
    t = y / (H - 1)
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]
        t1, c1 = stops[i + 1]
        if t0 <= t <= t1:
            f = (t - t0) / (t1 - t0)
            px_color = tuple(int(c0[k] + (c1[k] - c0[k]) * f) for k in range(3))
            break
    for x in range(W):
        px[x, y] = px_color
draw = ImageDraw.Draw(img, "RGBA")

# ---------- sun + glow ----------
sun_cx, sun_cy, sun_r = 540, 400, 140
for r, alpha in [(260, 40), (210, 70), (175, 110)]:
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([sun_cx - r, sun_cy - r, sun_cx + r, sun_cy + r], fill=(255, 190, 90, alpha))
    glow = glow.filter(ImageFilter.GaussianBlur(30))
    img.paste(Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB"), (0, 0))
draw = ImageDraw.Draw(img, "RGBA")
draw.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r],
             fill=(255, 209, 102, 255))

# ---------- skyline silhouette ----------
SKY = (22, 10, 36, 255)
base = 1080
x = -20
while x < W + 20:
    bw = random.randint(70, 150)
    bh = random.randint(150, 300)
    draw.rectangle([x, base - bh, x + bw, base], fill=SKY)
    # lit windows
    for _ in range(bw * bh // 900):
        wx = random.randint(x + 8, x + bw - 12)
        wy = random.randint(base - bh + 10, base - 14)
        draw.rectangle([wx, wy, wx + 6, wy + 8], fill=(255, 209, 102, 200))
    x += bw + random.randint(2, 14)

# ---------- ghost: big, centre stage, glowing ----------
ghost = Image.open(GHOST).convert("RGBA")
ghost = ghost.resize((440, 440), Image.LANCZOS)
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([540 - 250, 560 - 250, 540 + 250, 560 + 250], fill=(255, 255, 255, 90))
glow = glow.filter(ImageFilter.GaussianBlur(60))
img = Image.alpha_composite(img.convert("RGBA"), glow)
img.paste(ghost, (540 - 220, 340), ghost)
draw = ImageDraw.Draw(img, "RGBA")

# ---------- captions ----------
def fit_font(text, max_w, start):
    size = start
    while size > 20:
        f = ImageFont.truetype(BOLD, size)
        if draw.textbbox((0, 0), text, font=f)[2] <= max_w:
            return f
        size -= 4
    return ImageFont.truetype(BOLD, size)

def caption(text, y, size, fill=(255, 255, 255, 255)):
    f = fit_font(text, 980, size)
    bbox = draw.textbbox((0, 0), text, font=f, stroke_width=8)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (W - tw) / 2 - bbox[0]
    draw.text((x + 4, y + 5), text, font=f, fill=(0, 0, 0, 220), stroke_width=8, stroke_fill=(0, 0, 0, 220))
    draw.text((x, y), text, font=f, fill=fill, stroke_width=8, stroke_fill=(0, 0, 0, 255))
    return th

caption("WAITED 13 YEARS", 55, 108)
caption("FOR GTA 6", 175, 108)

# bottom band + pitch
draw.rectangle([0, 852, W, H], fill=(0, 0, 0, 110))
caption("MEANWHILE, MY AGENT", 868, 76)
caption("EARNS ON MAKE.FUN", 952, 82, fill=(255, 209, 102, 255))

img.convert("RGB").save(OUT, "PNG")
print("wrote", OUT)
