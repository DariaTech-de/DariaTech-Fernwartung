#!/usr/bin/env python3
"""Generate DariaTech brand assets (logo crop + reconstructed icon mark)."""
import os
from PIL import Image, ImageDraw

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "source-logo.png")
GREEN = (9, 37, 15)
TEAL = (1, 196, 166)
SS = 4  # supersample factor

# --- Icon mark geometry, normalized 0..100 (measured from the original) ---
# Sharp "<" chevron (parallelogram bars, mitered tip + flat-cut ends).
CHEV = [
    (8, 50),    # outer tip (left point)
    (52, 4),    # upper bar, outer top corner
    (68, 20),   # upper bar, end cut -> inner corner
    (33, 50),   # inner notch (points right)
    (68, 80),   # lower bar, end cut -> inner corner
    (52, 96),   # lower bar, outer bottom corner
]
# Solid square rotated 45 deg, centered right of the chevron mouth.
DIA = [(77, 27), (100, 50), (77, 73), (54, 50)]

# overall content bounds of the mark in normalized space
MARK_MINX, MARK_MAXX = 8.0, 100.0
MARK_MINY, MARK_MAXY = 4.0, 96.0


def draw_mark(size, bg=None, pad_frac=0.16, fg=TEAL):
    """Return RGBA image (size x size) with the mark. bg=None -> transparent."""
    S = size * SS
    img = Image.new("RGBA", (S, S), (bg + (255,)) if bg else (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pad = S * pad_frac
    content = S - 2 * pad
    mw = MARK_MAXX - MARK_MINX
    mh = MARK_MAXY - MARK_MINY
    scale = content / max(mw, mh)
    # center the mark bounding box
    ox = pad + (content - mw * scale) / 2 - MARK_MINX * scale
    oy = pad + (content - mh * scale) / 2 - MARK_MINY * scale

    def N(p):
        return (ox + p[0] * scale, oy + p[1] * scale)

    d.polygon([N(p) for p in CHEV], fill=fg)
    d.polygon([N(p) for p in DIA], fill=fg)

    return img.resize((size, size), Image.LANCZOS)


def rounded(img, radius_frac=0.18):
    """Apply rounded-corner mask to a square RGBA image."""
    S = img.size[0]
    big = S * SS
    mask = Image.new("L", (big, big), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, big, big],
                                           radius=int(big * radius_frac), fill=255)
    mask = mask.resize((S, S), Image.LANCZOS)
    out = img.copy()
    out.putalpha(mask)
    return out


if __name__ == "__main__":
    out = "/tmp/brand_out"
    os.makedirs(out, exist_ok=True)
    # preview: icon (rounded green square) + foreground
    icon = draw_mark(512, bg=GREEN, pad_frac=0.20)
    rounded(icon, 0.20).save(f"{out}/icon_preview.png")
    draw_mark(512, bg=None, pad_frac=0.30).save(f"{out}/foreground_preview.png")
    # logo crop (green panel)
    im = Image.open(SRC).convert("RGB")
    px = im.load(); W, H = im.size
    def is_green(p): return abs(p[0]-9) < 18 and abs(p[1]-37) < 20 and abs(p[2]-15) < 18
    minx, miny, maxx, maxy = W, H, 0, 0
    for y in range(0, H, 2):
        for x in range(0, W, 2):
            if is_green(px[x, y]):
                minx = min(minx, x); maxx = max(maxx, x)
                miny = min(miny, y); maxy = max(maxy, y)
    logo = im.crop((minx, miny, maxx + 1, maxy + 1))
    logo.save(f"{out}/logo_full.png")
    print("logo size", logo.size)
    print("done")
