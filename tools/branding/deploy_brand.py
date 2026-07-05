#!/usr/bin/env python3
"""Generate and deploy all DariaTech brand assets into the repo."""
import json, os, re
from PIL import Image, ImageDraw, ImageFont
import gen_brand as G  # draw_mark, GREEN, TEAL, rounded, SS

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GREEN = G.GREEN
SRC = G.SRC


def square_icon(size, opaque=True, radius=0.0):
    """Green square with teal mark. radius>0 -> rounded corners (transparent)."""
    img = G.draw_mark(size, bg=GREEN, pad_frac=0.20)
    if radius > 0:
        img = G.rounded(img, radius)
    if opaque:
        bg = Image.new("RGB", img.size, GREEN)
        bg.paste(img, (0, 0), img)
        return bg
    return img


def foreground(size):
    """Transparent canvas, teal mark in the adaptive-icon safe zone."""
    return G.draw_mark(size, bg=None, pad_frac=0.30)


def circular(size):
    img = square_icon(size, opaque=False, radius=0.0)  # rounded=0 -> sharp square w/ alpha
    # rebuild as full green square then mask to circle
    base = Image.new("RGBA", (size, size), GREEN + (255,))
    mark = G.draw_mark(size, bg=None, pad_frac=0.20)
    base.paste(mark, (0, 0), mark)
    big = size * G.SS
    mask = Image.new("L", (big, big), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, big, big], fill=255)
    base.putalpha(mask.resize((size, size), Image.LANCZOS))
    return base


def save(img, path):
    full = os.path.join(REPO, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    img.save(full)
    print("wrote", path, img.size)


def load_font(size, bold=True):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def synth_logo(width=1200):
    """Banner fallback when the original logo scan is unavailable:
    teal mark + 'DariaTech / IT SYSTEMHAUS' wordmark on brand green."""
    W, H = width, round(width * 0.25)
    img = Image.new("RGB", (W, H), GREEN)
    mark = G.draw_mark(round(H * 0.70), bg=None, pad_frac=0.02)
    mx, my = round(W * 0.045), (H - mark.size[1]) // 2
    img.paste(mark, (mx, my), mark)
    d = ImageDraw.Draw(img)
    tx = mx + mark.size[0] + round(W * 0.045)
    f1 = load_font(round(H * 0.38))
    f2 = load_font(round(H * 0.13))
    d.text((tx, round(H * 0.20)), "DariaTech", font=f1, fill=(255, 255, 255))
    d.text((tx + round(H * 0.02), round(H * 0.63)),
           " ".join("IT SYSTEMHAUS"), font=f2, fill=G.TEAL)
    return img


def wordmark_label(width=400, height=100):
    """Transparent 'DariaTech Fernwartung' label for the portable installer."""
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    mark = G.draw_mark(round(height * 0.66), bg=None, pad_frac=0.02)
    my = (height - mark.size[1]) // 2
    img.paste(mark, (4, my), mark)
    d = ImageDraw.Draw(img)
    tx = 4 + mark.size[0] + round(height * 0.20)
    d.text((tx, round(height * 0.16)), "DariaTech",
           font=load_font(round(height * 0.34)), fill=(255, 255, 255, 255))
    d.text((tx, round(height * 0.56)), "Fernwartung",
           font=load_font(round(height * 0.22), bold=False), fill=G.TEAL + (255,))
    return img


def tray_template(size, color):
    """Monochrome mark for macOS menu-bar template icons."""
    mark = G.draw_mark(size, bg=None, pad_frac=0.10, fg=color)
    return mark


def main():
    # ---------- In-app Flutter ----------
    # logo: crop green panel from the original scan if present, else synthesize
    if os.path.exists(SRC):
        im = Image.open(SRC).convert("RGB"); px = im.load(); W, H = im.size
        def is_green(p): return abs(p[0]-9) < 18 and abs(p[1]-37) < 20 and abs(p[2]-15) < 18
        minx, miny, maxx, maxy = W, H, 0, 0
        for y in range(0, H, 2):
            for x in range(0, W, 2):
                if is_green(px[x, y]):
                    minx = min(minx, x); maxx = max(maxx, x)
                    miny = min(miny, y); maxy = max(maxy, y)
        logo = im.crop((minx, miny, maxx + 1, maxy + 1))
        lw = 1200
        logo = logo.resize((lw, round(lw * logo.size[1] / logo.size[0])), Image.LANCZOS)
    else:
        print("source-logo.png missing -> synthesizing banner logo")
        logo = synth_logo()
    save(logo, "flutter/assets/logo.png")

    save(square_icon(512, opaque=False, radius=0.20), "flutter/assets/icon.png")
    write_svg(os.path.join(REPO, "flutter/assets/icon.svg"))
    print("wrote flutter/assets/icon.svg")

    # ---------- res/ (Linux + master) ----------
    save(square_icon(1024, opaque=True), "res/icon.png")
    for s, name in [(32, "32x32.png"), (64, "64x64.png"),
                    (128, "128x128.png"), (256, "128x128@2x.png")]:
        save(square_icon(s, opaque=True), f"res/{name}")
    ico_base = square_icon(256, opaque=True)
    ico_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    for path in ["res/icon.ico", "flutter/windows/runner/resources/app_icon.ico"]:
        full = os.path.join(REPO, path)
        ico_base.save(full, sizes=ico_sizes)
        print("wrote", path)

    # ---------- Linux scalable icon ----------
    write_svg(os.path.join(REPO, "res/scalable.svg"))
    print("wrote res/scalable.svg")

    # ---------- macOS .icns (rounded squircle) ----------
    icns = square_icon(1024, opaque=False, radius=0.22)
    full = os.path.join(REPO, "flutter/macos/Runner/AppIcon.icns")
    icns.save(full)
    print("wrote flutter/macos/Runner/AppIcon.icns")
    save(square_icon(1024, opaque=False, radius=0.22), "res/mac-icon.png")

    # ---------- macOS menu-bar (template) icons ----------
    save(tray_template(44, (255, 255, 255)), "res/mac-tray-dark-x2.png")
    save(tray_template(44, (0, 0, 0)), "res/mac-tray-light-x2.png")

    # ---------- Windows portable installer label ----------
    save(wordmark_label(), "libs/portable/src/res/label.png")

    # ---------- iOS (opaque, no alpha) ----------
    ios_dir = "flutter/ios/Runner/Assets.xcassets/AppIcon.appiconset"
    with open(os.path.join(REPO, ios_dir, "Contents.json")) as f:
        contents = json.load(f)
    for entry in contents.get("images", []):
        fn = entry.get("filename")
        if not fn:
            continue
        m = re.match(r"Icon-App-([\d.]+)x[\d.]+@(\d)x\.png", fn)
        if not m:
            continue
        size = round(float(m.group(1)) * int(m.group(2)))
        save(square_icon(size, opaque=True), f"{ios_dir}/{fn}")

    # ---------- Android ----------
    and_res = "flutter/android/app/src/main/res"
    dens = {"mdpi": 1, "hdpi": 1.5, "xhdpi": 2, "xxhdpi": 3, "xxxhdpi": 4}
    for d, m in dens.items():
        ic = round(48 * m)
        fg = round(108 * m)
        save(square_icon(ic, opaque=True), f"{and_res}/mipmap-{d}/ic_launcher.png")
        save(circular(ic), f"{and_res}/mipmap-{d}/ic_launcher_round.png")
        save(foreground(fg), f"{and_res}/mipmap-{d}/ic_launcher_foreground.png")
        # splash screen image referenced by drawable/launch_background.xml
        save(square_icon(round(160 * m), opaque=False, radius=0.20),
             f"{and_res}/mipmap-{d}/launch_image.png")
    # background color -> green
    bgxml = os.path.join(REPO, and_res, "values/ic_launcher_background.xml")
    with open(bgxml, "w") as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
                '    <color name="ic_launcher_background">#09250F</color>\n</resources>\n')
    print("wrote", and_res + "/values/ic_launcher_background.xml")


def write_svg(path):
    def pts(poly):
        return " ".join(f"{x},{y}" for x, y in poly)
    teal = "#01C4A6"
    green = "#09250F"
    # map mark (8..100 x, 4..96 y) into a 0..100 viewBox with padding 12
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect width="100" height="100" rx="20" fill="{green}"/>
  <g transform="translate(16 16) scale(0.68) translate(-8 -4)">
    <polygon points="{pts(G.CHEV)}" fill="{teal}"/>
    <polygon points="{pts(G.DIA)}" fill="{teal}"/>
  </g>
</svg>
'''
    with open(path, "w") as f:
        f.write(svg)


if __name__ == "__main__":
    main()
    print("ALL DONE")
