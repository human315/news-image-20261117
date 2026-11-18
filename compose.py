#!/usr/bin/env python3
"""Compose the news-image-20261117 front page (1024x1024) from 6 generated panels."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W, H = 1024, 1024
PAPER = (245, 240, 230)
INK = (20, 20, 20)
RED = (178, 34, 34)
WHITE = (255, 255, 255)
DARK = (30, 30, 34)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FSB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FSR = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def cover_crop(im, tw, th):
    """Center-crop to target aspect, then resize (deterministic)."""
    sw, sh = im.size
    ta, sa = tw / th, sw / sh
    if sa > ta:
        nw = int(sh * ta)
        x = (sw - nw) // 2
        im = im.crop((x, 0, x + nw, sh))
    else:
        nh = int(sw / ta)
        y = (sh - nh) // 2
        im = im.crop((0, y, sw, y + nh))
    return im.resize((tw, th), Image.LANCZOS)

PANELS = [
    ("media-generation-panel1-kerch-bridge-0-4dc0c3d7-34fc-4eb7-b550-4db1c8ec8ca0.png",
     "UKRAINE WAR", "Kerch Bridge hit again; Kyiv bridges struck in reply"),
    ("media-generation-panel2-hormuz-tanker-0-bcf011b0-6f53-459a-aaf3-32ccbb196361.png",
     "US \u2013 IRAN", "Drone hits US base in Bahrain; tanker ablaze near Hormuz"),
    ("media-generation-panel3-shenzhen-summit-0-31509066-598c-4acc-b987-93ea540dcc78.png",
     "SUMMIT", "Xi, Trump and Putin to meet in Shenzhen on Thursday"),
    ("media-generation-panel4-cyberattack-0-8caad714-fae2-4e78-ad42-b4a0ba764e1b.png",
     "CYBERATTACK", "Malware in Optimizely code hits 178 major websites"),
    ("media-generation-panel5-westbank-0-9e72f758-1805-4bfd-b0ef-23c141080856.png",
     "WEST BANK", "UK sanctions settlement builders; settler kills woman, 72"),
    ("media-generation-panel6-japan-jets-0-64882f74-4bc4-4c9e-add7-b30027f8c4ad.png",
     "JAPAN", "Jets scramble as suspected Russian planes enter airspace"),
]

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header ----
    d.rectangle([0, 0, W, 118], fill=PAPER)
    d.line([16, 112, W - 16, 112], fill=INK, width=3)
    d.line([16, 118, W - 16, 118], fill=INK, width=1)
    f_kick = font(FB, 24)
    f_date = font(FSB, 42)
    t1 = "THE WORLD IN ONE IMAGE"
    d.text(((W - d.textlength(t1, font=f_kick)) / 2, 12), t1, font=f_kick, fill=RED)
    t2 = "TUESDAY 17 NOVEMBER 2026"
    d.text(((W - d.textlength(t2, font=f_date)) / 2, 46), t2, font=f_date, fill=INK)

    # ---- grid: 2 cols x 3 rows ----
    mx, gutter = 16, 12
    pw = (W - 2 * mx - gutter) // 2          # 490
    ph = 274
    ih = 196                                   # image height
    ch = ph - ih                               # caption height 78
    top = 130
    f_lab = font(FB, 16)
    f_head = font(FB, 20)
    for i, (fname, label, headline) in enumerate(PANELS):
        col, row = i % 2, i // 2
        x = mx + col * (pw + gutter)
        y = top + row * (ph + gutter)
        src = Image.open(os.path.join(ASSETS, fname)).convert("RGB")
        img.paste(cover_crop(src, pw, ih), (x, y))
        d.rectangle([x, y, x + pw - 1, y + ih - 1], outline=INK, width=2)
        # caption block
        cy = y + ih
        d.rectangle([x, cy, x + pw, cy + ch], fill=WHITE)
        d.rectangle([x, cy, x + pw - 1, cy + ch - 1], outline=INK, width=1)
        d.text((x + 10, cy + 7), label, font=f_lab, fill=RED)
        lines = wrap(d, headline, f_head, pw - 20)
        ly = cy + 30
        for ln in lines[:2]:
            d.text((x + 10, ly), ln, font=f_head, fill=INK)
            ly += 24

    # ---- footer strip ----
    fy = 976
    d.rectangle([0, fy, W, H], fill=DARK)
    f_foot = font(FR, 15)
    ft = "ALSO: EU sanctions 12 people and 101 entities  \u00b7  128 nations at UN debate ban on autonomous weapons"
    d.text(((W - d.textlength(ft, font=f_foot)) / 2, fy + 14), ft, font=f_foot, fill=(235, 230, 220))

    return img

if __name__ == "__main__":
    out = build()
    out_path = os.path.join(HERE, "entry.png")
    out.save(out_path, "PNG", optimize=True)
    size = os.path.getsize(out_path)
    print("PNG bytes:", size)
    if size > 1048576:
        out.save(out_path, "JPEG", quality=88, optimize=True)
        print("saved as JPEG, bytes:", os.path.getsize(out_path))
    print("done:", out_path, out.size)
