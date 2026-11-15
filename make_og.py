#!/usr/bin/env python3
"""og.png 1200×630 — denim×hay honky-tonk marquee art for The Donkey Barn. Shop identity only, zero builder tokens."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "og.png")

def font(path_names, size):
    bases = ["/System/Library/Fonts/Supplemental/", "/System/Library/Fonts/"]
    for b in bases:
        for n in path_names:
            p = b + n
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except Exception:
                    pass
    return ImageFont.load_default()

NIGHT=(19,26,44); DENIM=(28,39,64); BONE=(244,239,225); MIST=(174,182,196)
HAY=(233,182,76); HAY2=(243,205,116)

img = Image.new("RGB", (W, H), NIGHT)
d = ImageDraw.Draw(img, "RGBA")

# denim gradient wash
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=(int(14 + 16 * t), int(20 + 21 * t), int(36 + 32 * t)))

# faint diagonal hay stitch lines
for x in range(-H, W, 24):
    d.line([(x, H), (x + H, 0)], fill=(233, 182, 76, 10), width=2)

# marquee bulb rows — top and bottom
def bulbs(y):
    for r, a in [(14, 14), (9, 26)]:
        for x in range(26, W - 12, 44):
            d.ellipse((x - r, y - r, x + r, y + r), fill=(233, 182, 76, a))
    for x in range(26, W - 12, 44):
        d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=HAY)
bulbs(34); bulbs(H - 34)

f_eye = font(["Arial Bold.ttf", "Helvetica.ttc"], 22)
f_word = font(["Georgia Bold.ttf", "Arial Bold.ttf"], 108)
f_sub = font(["Arial Bold.ttf", "Helvetica.ttc"], 34)
f_quote = font(["Georgia Italic.ttf", "Georgia.ttf"], 31)
f_line = font(["Arial.ttf", "Helvetica.ttc"], 23)

# eyebrow
d.text((76, 84), "B E L L E V U E ,   N E B R A S K A   ·   O M A H A   M E T R O", font=f_eye, fill=HAY)

# wordmark, auto-fit
word = "THE DONKEY BARN"
size = 108
while size > 60:
    fw = font(["Georgia Bold.ttf", "Arial Bold.ttf"], size)
    if d.textlength(word, font=fw) <= 1048:
        break
    size -= 4
d.text((76, 126), word, font=fw, fill=BONE)

# subline
d.text((78, 262), "COUNTRY BAR  ·  GRILL  ·  LIVE MUSIC  ·  LINE DANCING", font=f_sub, fill=HAY)

# concept quote (their own promo copy, verbatim, split over three lines)
qlines = [
    "\u201cCountry bar, restaurant, and live music destination",
    "featuring burgers, signature grub, beer, cocktails,",
    "a dance floor, and line dancing.\u201d",
]
qy = 330
for ql in qlines:
    d.text((78, qy), ql, font=f_quote, fill=(244, 239, 225, 200))
    qy += 44

# facts line
d.line([(76, 528), (1124, 528)], fill=(244, 239, 225, 60), width=2)
d.text((76, 552), "2902 Samson Way  ·  Bellevue, NE 68123  ·  Open Wed\u2013Sat  ·  late Fri\u2013Sat", font=f_line, fill=MIST)

img.save(OUT, "PNG")
print("wrote", OUT, os.path.getsize(OUT), "bytes")
