#!/usr/bin/env python3
"""ugliness-review evidence kit.

Deterministic evidence collectors for visual review. No network, no API keys.

Subcommands:
  kit         produce the standard evidence set (gray, blur, thumb wall,
              silhouette wall, color stats, manifest)
  silhouette  pure-black silhouette(s) + wall
  thumbs      thumbnail wall at a given size (default 64px)
  gray        grayscale copy
  blur        squint / gaussian blur copy
  crop        zoomed crop of a region (tangent check)
  colors      dominant colors + saturated-area estimate
  grid        grid + margin overlay
  contrast    WCAG contrast ratio between two sampled points
  palette     distinct color count + top colors (pixel-art palette)
  lightness   Lab L* difference between two sampled points (H-R7)

Examples:
  python scripts/evidence.py kit ui.png renders/*.png -o evidence
  python scripts/evidence.py silhouette assets/ -o evidence
  python scripts/evidence.py crop ui.png --box 900,380,1060,500 --zoom 3
  python scripts/evidence.py contrast ui.png --fg 300,640 --bg 200,700

Only reads raster files (PNG / JPG / WebP / BMP / GIF). Requires Pillow:
  pip install pillow
"""

from __future__ import annotations

import argparse
from collections import Counter
import colorsys
import math
import sys
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

VERSION = "0.3.0"
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"}
DEFAULT_OUT = "evidence"
SAT_THRESHOLD = 0.35  # HSV saturation above this counts as "saturated" for area %


# ---------------------------------------------------------------- helpers

def die(msg: str) -> "NoReturn":
    print(f"error: {msg}", file=sys.stderr)
    raise SystemExit(2)


def load(path: Path) -> Image.Image:
    try:
        im = Image.open(path)
        im = ImageOps.exif_transpose(im)
    except Exception as exc:  # noqa: BLE001
        die(f"cannot open {path}: {exc}")
    return im


def as_rgba(im: Image.Image) -> Image.Image:
    return im if im.mode == "RGBA" else im.convert("RGBA")


def on_white(im: Image.Image) -> Image.Image:
    if im.mode in ("RGBA", "LA", "P"):
        base = Image.new("RGBA", im.size, (255, 255, 255, 255))
        rgba = as_rgba(im)
        base.alpha_composite(rgba)
        return base.convert("RGB")
    return im.convert("RGB")


def fit(im: Image.Image, size: int) -> Image.Image:
    scale = size / max(im.width, im.height)
    w = max(1, round(im.width * scale))
    h = max(1, round(im.height * scale))
    return im.resize((w, h), Image.LANCZOS)


def save(im: Image.Image, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path)
    return path


def expand_inputs(paths: list[str]) -> list[Path]:
    out: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            out.extend(sorted(q for q in p.iterdir() if q.suffix.lower() in IMAGE_EXTS))
        elif p.is_file():
            out.append(p)
        else:
            die(f"input not found: {p}")
    if not out:
        die("no raster images found in inputs")
    return out


def parse_point(text: str) -> tuple[int, int]:
    try:
        x, y = text.split(",")
        return int(x), int(y)
    except Exception:  # noqa: BLE001
        die(f"point must look like x,y — got: {text}")


def parse_box(text: str) -> tuple[int, int, int, int]:
    try:
        x1, y1, x2, y2 = (int(v) for v in text.split(","))
        return x1, y1, x2, y2
    except Exception:  # noqa: BLE001
        die(f"box must look like x1,y1,x2,y2 — got: {text}")


def label_font(height: int) -> ImageFont.ImageFont:
    try:
        return ImageFont.load_default(size=max(10, height))
    except TypeError:
        return ImageFont.load_default()


def make_wall(items: list[tuple[Image.Image, str]], cell: int, cols: int,
              pad: int = 12, label_h: int = 18) -> Image.Image:
    """Compose a labeled contact sheet. Items are (image, short label)."""
    n = len(items)
    cols = max(1, min(cols, n or 1))
    rows = max(1, math.ceil(n / cols))
    cell_h = cell + label_h
    width = cols * (cell + pad) + pad
    height = rows * (cell_h + pad) + pad
    canvas = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    font = label_font(label_h - 4)
    for i, (im, label) in enumerate(items):
        row, col = divmod(i, cols)
        x = pad + col * (cell + pad)
        y = pad + row * (cell_h + pad)
        thumb = on_white(fit(im, cell))
        ox = x + (cell - thumb.width) // 2
        oy = y + (cell - thumb.height) // 2
        canvas.paste(thumb, (ox, oy))
        draw.text((x + 2, y + cell + 1), label, fill=(60, 60, 60, 255), font=font)
    return canvas


# ---------------------------------------------------------------- operations

def to_silhouette(im: Image.Image, threshold: str = "auto",
                  invert: bool = False, transparent: bool = False) -> Image.Image:
    """Pure-black silhouette. Uses alpha when present, else luminance threshold."""
    rgba = as_rgba(im)
    has_alpha = "A" in im.getbands() or im.mode in ("RGBA", "LA", "P")
    mask = None
    if has_alpha:
        alpha = rgba.getchannel("A")
        if alpha.getextrema()[0] < 250:  # real transparency present
            mask = alpha.point(lambda a: 255 if a > 16 else 0)
    if mask is None:
        gray = on_white(im).convert("L")
        if threshold == "auto":
            bg = border_luminance(gray)
            thr = max(8, round(bg * 0.90)) if bg >= 160 else otsu_threshold(gray)
        else:
            try:
                thr = int(threshold)
            except ValueError:
                die(f"threshold must be 'auto' or 0-255, got: {threshold}")
        if invert:
            mask = gray.point(lambda v: 255 if v >= thr else 0)
        else:
            mask = gray.point(lambda v: 255 if v < thr else 0)
    bg = (0, 0, 0, 0) if transparent else (255, 255, 255, 255)
    out = Image.new("RGBA", im.size, bg)
    black = Image.new("RGBA", im.size, (0, 0, 0, 255))
    out.paste(black, (0, 0), mask)
    return out


def border_luminance(gray: Image.Image) -> int:
    """Median luminance of 8x8 corner patches — a background estimate."""
    w, h = gray.size
    values: list[int] = []
    for box in ((0, 0, 8, 8), (w - 8, 0, w, 8), (0, h - 8, 8, h), (w - 8, h - 8, w, h)):
        values.extend(gray.crop(box).getdata())
    values.sort()
    return values[len(values) // 2]


def otsu_threshold(gray: Image.Image) -> int:
    hist = gray.histogram()
    total = sum(hist)
    sum_all = sum(i * h for i, h in enumerate(hist))
    sum_b = 0.0
    w_b = 0
    best_var = -1.0
    best = 127
    for t in range(256):
        w_b += hist[t]
        if w_b == 0:
            continue
        w_f = total - w_b
        if w_f == 0:
            break
        sum_b += t * hist[t]
        m_b = sum_b / w_b
        m_f = (sum_all - sum_b) / w_f
        var = w_b * w_f * (m_b - m_f) ** 2
        if var > best_var:
            best_var = var
            best = t
    return best


def color_stats(im: Image.Image, top: int = 6) -> dict:
    rgb = on_white(im).convert("RGB")
    small = rgb.copy()
    small.thumbnail((480, 480), Image.LANCZOS)
    quant = small.quantize(colors=max(1, top))
    palette = quant.getpalette() or []
    counts = sorted(quant.getcolors() or [], reverse=True)
    total = sum(c for c, _ in counts) or 1
    tops = []
    for count, idx in counts:
        r, g, b = palette[idx * 3: idx * 3 + 3]
        tops.append({"hex": f"#{r:02x}{g:02x}{b:02x}", "pct": round(100 * count / total, 1)})
    sat = rgb.copy()
    sat.thumbnail((320, 320), Image.LANCZOS)
    pixels = list(sat.getdata())
    n = len(pixels) or 1
    saturated = 0
    for r, g, b in pixels:
        _, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if s >= SAT_THRESHOLD and v >= 0.15:
            saturated += 1
    return {
        "top": tops,
        "saturated_pct": round(100 * saturated / n, 1),
        "size": im.size,
    }


def squint(im: Image.Image, radius: int | None = None) -> Image.Image:
    if radius is None:
        radius = max(2, round(min(im.size) * 0.012))
    return im.filter(ImageFilter.GaussianBlur(radius))


def grid_overlay(im: Image.Image, step: int = 8, margin_pct: float = 5.0) -> Image.Image:
    base = as_rgba(im)
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    w, h = base.size
    for x in range(0, w, max(1, step)):
        draw.line([(x, 0), (x, h)], fill=(0, 120, 255, 40), width=1)
    for y in range(0, h, max(1, step)):
        draw.line([(0, y), (w, y)], fill=(0, 120, 255, 40), width=1)
    mx = round(w * margin_pct / 100)
    my = round(h * margin_pct / 100)
    draw.rectangle([mx, my, w - mx, h - my], outline=(220, 30, 30, 170), width=2)
    return Image.alpha_composite(base, overlay)


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    def channel(c: int) -> float:
        v = c / 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast_ratio(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    la, lb = relative_luminance(a), relative_luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def sample_avg(im: Image.Image, point: tuple[int, int], radius: int = 2) -> tuple[int, int, int]:
    x, y = point
    rgb = on_white(im).convert("RGB")
    x0, y0 = max(0, x - radius), max(0, y - radius)
    x1, y1 = min(rgb.width, x + radius + 1), min(rgb.height, y + radius + 1)
    patch = rgb.crop((x0, y0, x1, y1))
    pixels = list(patch.getdata())
    n = len(pixels) or 1
    return (
        sum(p[0] for p in pixels) // n,
        sum(p[1] for p in pixels) // n,
        sum(p[2] for p in pixels) // n,
    )


def lab_l(rgb: tuple[int, int, int]) -> float:
    """CIELAB L* (0-100) of an sRGB color."""
    def channel(c: int) -> float:
        v = c / 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

    r, g, b = (channel(v) for v in rgb)
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return 116 * (y ** (1 / 3)) - 16 if y > 0.008856 else 903.3 * y


# ---------------------------------------------------------------- commands

def cmd_silhouette(args: argparse.Namespace) -> None:
    inputs = expand_inputs(args.inputs)
    outdir = Path(args.out)
    items = []
    for i, path in enumerate(inputs, 1):
        im = load(path)
        sil = to_silhouette(im, threshold=args.threshold, invert=args.invert,
                            transparent=args.transparent)
        save(sil, outdir / f"{path.stem}_silhouette.png")
        items.append((sil, str(i)))
        print(f"[{i}] {path.name} -> {path.stem}_silhouette.png")
    if len(items) > 1 or args.wall:
        wall = make_wall(items, cell=args.cell, cols=args.cols)
        save(wall, outdir / "wall_silhouette.png")
        print(f"wall -> {outdir / 'wall_silhouette.png'} (labels = input order)")
    print("reminder: 1-second readability test — if you cannot name an asset from its silhouette, it fails A-R7.")


def cmd_thumbs(args: argparse.Namespace) -> None:
    inputs = expand_inputs(args.inputs)
    outdir = Path(args.out)
    items = []
    for i, path in enumerate(inputs, 1):
        im = load(path)
        items.append((im, str(i)))
    wall = make_wall(items, cell=args.size, cols=args.cols)
    dest = save(wall, outdir / f"wall_thumbs_{args.size}.png")
    print(f"wall -> {dest}")
    for i, path in enumerate(inputs, 1):
        print(f"  [{i}] {path.name}")
    print(f"reminder: check at {args.size}px — if an asset cannot be recognized, it fails A-R7.")


def cmd_gray(args: argparse.Namespace) -> None:
    inputs = expand_inputs(args.inputs)
    outdir = Path(args.out)
    for path in inputs:
        im = load(path)
        dest = save(im.convert("L"), outdir / f"{path.stem}_gray.png")
        print(f"{path.name} -> {dest}")


def cmd_blur(args: argparse.Namespace) -> None:
    inputs = expand_inputs(args.inputs)
    outdir = Path(args.out)
    for path in inputs:
        im = load(path)
        radius = args.radius if args.radius else max(2, round(min(im.size) * 0.012))
        dest = save(squint(im, radius), outdir / f"{path.stem}_blur.png")
        print(f"{path.name} -> {dest} (radius={radius}px)")


def cmd_crop(args: argparse.Namespace) -> None:
    path = Path(args.input)
    if not path.is_file():
        die(f"input not found: {path}")
    im = load(path)
    box = parse_box(args.box)
    x1, y1, x2, y2 = box
    if not (0 <= x1 < x2 <= im.width and 0 <= y1 < y2 <= im.height):
        die(f"box {box} out of bounds for {im.width}x{im.height}")
    zoom = max(1, args.zoom)
    crop = im.crop(box)
    crop = crop.resize((crop.width * zoom, crop.height * zoom), Image.LANCZOS)
    dest = save(crop, Path(args.out) / f"{path.stem}_crop_{x1}-{y1}-{x2}-{y2}_x{zoom}.png")
    print(f"crop -> {dest} ({crop.width}x{crop.height})")


def cmd_colors(args: argparse.Namespace) -> None:
    inputs = expand_inputs(args.inputs)
    for path in inputs:
        stats = color_stats(load(path), top=args.top)
        print(f"\n{path.name}  {stats['size'][0]}x{stats['size'][1]}")
        print(f"  saturated area (S>={SAT_THRESHOLD}): {stats['saturated_pct']}%")
        for c in stats["top"]:
            print(f"  {c['hex']}  {c['pct']}%")
    print("\nreminder: A-R6 — saturated area should stay <=15% and only one signal color may be on duty.")


def cmd_grid(args: argparse.Namespace) -> None:
    inputs = expand_inputs(args.inputs)
    outdir = Path(args.out)
    for path in inputs:
        im = load(path)
        dest = save(grid_overlay(im, step=args.step, margin_pct=args.margin),
                    outdir / f"{path.stem}_grid.png")
        print(f"{path.name} -> {dest} (step={args.step}px, margin={args.margin}%)")


def cmd_contrast(args: argparse.Namespace) -> None:
    path = Path(args.input)
    if not path.is_file():
        die(f"input not found: {path}")
    im = load(path)
    fg_pt, bg_pt = parse_point(args.fg), parse_point(args.bg)
    fg, bg = sample_avg(im, fg_pt), sample_avg(im, bg_pt)
    ratio = contrast_ratio(fg, bg)
    verdict = "AA normal text (>=4.5)" if ratio >= 4.5 else (
        "AA large text / non-text (>=3)" if ratio >= 3 else "FAIL (<3)")
    print(f"fg {fg_pt} #{fg[0]:02x}{fg[1]:02x}{fg[2]:02x}  bg {bg_pt} #{bg[0]:02x}{bg[1]:02x}{bg[2]:02x}")
    print(f"contrast ratio: {ratio:.2f}:1  -> {verdict}")
    canvas = as_rgba(im).copy()
    draw = ImageDraw.Draw(canvas)
    for pt, color in ((fg_pt, (220, 30, 30, 255)), (bg_pt, (30, 90, 220, 255))):
        x, y = pt
        draw.line([(x - 8, y), (x + 8, y)], fill=color, width=2)
        draw.line([(x, y - 8), (x, y + 8)], fill=color, width=2)
    draw.text((10, 10), f"contrast {ratio:.2f}:1", fill=(0, 0, 0, 255),
              font=label_font(18))
    dest = save(canvas, Path(args.out) / f"{path.stem}_contrast.png")
    print(f"annotated -> {dest}")


def cmd_kit(args: argparse.Namespace) -> None:
    inputs = expand_inputs(args.inputs)
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    thumb_items, sil_items, rows = [], [], []
    for i, path in enumerate(inputs, 1):
        im = load(path)
        gray = save(im.convert("L"), outdir / f"{path.stem}_gray.png")
        radius = args.blur if args.blur else max(2, round(min(im.size) * 0.012))
        blur = save(squint(im, radius), outdir / f"{path.stem}_blur.png")
        sil = to_silhouette(im)
        sil_path = save(sil, outdir / f"{path.stem}_silhouette.png")
        thumb_items.append((im, str(i)))
        sil_items.append((sil, str(i)))
        stats = color_stats(im, top=5)
        top_hex = ", ".join(c["hex"] for c in stats["top"][:3])
        rows.append((i, path.name, f"{im.width}x{im.height}",
                     f"{stats['saturated_pct']}%", top_hex))
        print(f"[{i}] {path.name}: gray, blur(r={radius}), silhouette, colors")
        _ = gray, blur, sil_path  # written above
    wall_t = save(make_wall(thumb_items, cell=args.thumb, cols=args.cols),
                  outdir / f"wall_thumbs_{args.thumb}.png")
    wall_s = save(make_wall(sil_items, cell=args.cell, cols=args.cols),
                  outdir / "wall_silhouette.png")
    manifest = outdir / "manifest.md"
    lines = [
        f"# Evidence manifest — {date.today().isoformat()}",
        "",
        f"Generated by `scripts/evidence.py` v{VERSION}. 数值为自动测量，判卷前请人工复核。",
        "",
        f"- thumb size: {args.thumb}px",
        f"- silhouette cell: {args.cell}px",
        f"- saturated threshold: S >= {SAT_THRESHOLD}",
        "",
        "| # | file | size | saturated area | top colors |",
        "| --- | --- | --- | --- | --- |",
    ]
    for i, name, size, sat, tops in rows:
        lines.append(f"| {i} | {name} | {size} | {sat} | {tops} |")
    lines += ["", f"- thumb wall: `{wall_t.name}`", f"- silhouette wall: `{wall_s.name}`", ""]
    manifest.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nkit -> {outdir}/  (manifest.md, gray, blur, silhouette, two walls)")


def cmd_palette(args: argparse.Namespace) -> None:
    inputs = expand_inputs(args.inputs)
    for path in inputs:
        im = load(path)
        if args.box:
            x1, y1, x2, y2 = parse_box(args.box)
            im = im.crop((x1, y1, x2, y2))
        rgba = as_rgba(im)
        counts: Counter = Counter()
        for pixel in rgba.getdata():
            if pixel[3] == 0:
                continue
            counts[pixel[:3]] += 1
        total = len(counts)
        pixels = sum(counts.values()) or 1
        print(f"{path.name}: {im.width}x{im.height} distinct colors = {total}")
        for (r, g, b), n in counts.most_common(args.top):
            print(f"  #{r:02x}{g:02x}{b:02x}  {100 * n / pixels:.1f}%")
    print("reminder: H-R4 — distinct colors must not exceed the project palette capacity.")


def cmd_lightness(args: argparse.Namespace) -> None:
    path = Path(args.input)
    if not path.is_file():
        die(f"input not found: {path}")
    im = load(path)
    a, b = parse_point(args.a), parse_point(args.b)
    ca, cb = sample_avg(im, a), sample_avg(im, b)
    la, lb = lab_l(ca), lab_l(cb)
    print(f"a {a} #{ca[0]:02x}{ca[1]:02x}{ca[2]:02x}  L*={la:.1f}")
    print(f"b {b} #{cb[0]:02x}{cb[1]:02x}{cb[2]:02x}  L*={lb:.1f}")
    print(f"delta L* = {abs(la - lb):.1f}  (H-R7 threshold: >=15)")


# ---------------------------------------------------------------- cli

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="evidence.py",
        description="ugliness-review evidence kit (deterministic, offline).",
    )
    p.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp: argparse.ArgumentParser, out: bool = True) -> None:
        sp.add_argument("inputs", nargs="+", help="image files or directories")
        if out:
            sp.add_argument("-o", "--out", default=DEFAULT_OUT, help="output directory")

    sp = sub.add_parser("kit", help="standard evidence set")
    common(sp)
    sp.add_argument("--thumb", type=int, default=64)
    sp.add_argument("--cell", type=int, default=96, help="silhouette cell size")
    sp.add_argument("--cols", type=int, default=6)
    sp.add_argument("--blur", type=int, default=0, help="0 = auto radius")
    sp.set_defaults(func=cmd_kit)

    sp = sub.add_parser("silhouette", help="pure-black silhouette(s)")
    common(sp)
    sp.add_argument("--threshold", default="auto", help="'auto' or 0-255")
    sp.add_argument("--invert", action="store_true", help="object is bright on dark")
    sp.add_argument("--transparent", action="store_true", help="transparent background")
    sp.add_argument("--cell", type=int, default=128)
    sp.add_argument("--cols", type=int, default=6)
    sp.add_argument("--wall", action="store_true", help="force wall even for one image")
    sp.set_defaults(func=cmd_silhouette)

    sp = sub.add_parser("thumbs", help="thumbnail wall")
    common(sp)
    sp.add_argument("--size", type=int, default=64)
    sp.add_argument("--cols", type=int, default=6)
    sp.set_defaults(func=cmd_thumbs)

    sp = sub.add_parser("gray", help="grayscale copy")
    common(sp)
    sp.set_defaults(func=cmd_gray)

    sp = sub.add_parser("blur", help="squint blur copy")
    common(sp)
    sp.add_argument("--radius", type=int, default=0, help="0 = auto")
    sp.set_defaults(func=cmd_blur)

    sp = sub.add_parser("crop", help="zoomed crop")
    sp.add_argument("input")
    sp.add_argument("--box", required=True, help="x1,y1,x2,y2 (pixels)")
    sp.add_argument("--zoom", type=int, default=3)
    sp.add_argument("-o", "--out", default=DEFAULT_OUT)
    sp.set_defaults(func=cmd_crop)

    sp = sub.add_parser("colors", help="dominant colors + saturated area")
    common(sp, out=False)
    sp.add_argument("--top", type=int, default=6)
    sp.set_defaults(func=cmd_colors)

    sp = sub.add_parser("grid", help="grid + margin overlay")
    common(sp)
    sp.add_argument("--step", type=int, default=8)
    sp.add_argument("--margin", type=float, default=5.0)
    sp.set_defaults(func=cmd_grid)

    sp = sub.add_parser("contrast", help="WCAG contrast between two points")
    sp.add_argument("input")
    sp.add_argument("--fg", required=True, help="x,y of foreground")
    sp.add_argument("--bg", required=True, help="x,y of background")
    sp.add_argument("-o", "--out", default=DEFAULT_OUT)
    sp.set_defaults(func=cmd_contrast)

    sp = sub.add_parser("palette", help="distinct color count (pixel-art palette)")
    common(sp, out=False)
    sp.add_argument("--box", help="x1,y1,x2,y2 region")
    sp.add_argument("--top", type=int, default=8)
    sp.set_defaults(func=cmd_palette)

    sp = sub.add_parser("lightness", help="Lab L* difference between two points")
    sp.add_argument("input")
    sp.add_argument("--a", required=True, help="x,y")
    sp.add_argument("--b", required=True, help="x,y")
    sp.set_defaults(func=cmd_lightness)

    return p


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
