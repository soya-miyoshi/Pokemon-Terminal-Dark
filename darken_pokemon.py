#!/usr/bin/env python3
"""
Darken Pokemon terminal images by detecting each image's base (background)
color and shifting it to a dark variant while preserving the Pokemon details.

Usage:
    python3 darken_pokemon.py [--target-brightness 0.15] [--dry-run] [--preview FILE]

Options:
    --target-brightness  How dark the base should become (0.0=black, 1.0=unchanged). Default: 0.15
    --dry-run            Only print what would be done, don't modify files.
    --preview FILE       Process a single file and save as FILE_dark.jpg for inspection.
    --backup             Copy originals to Images_backup/ before modifying.
"""

import argparse
import colorsys
import os
import shutil
import sys
from collections import Counter
from pathlib import Path

from PIL import Image

IMAGES_DIR = Path(__file__).parent / "pokemonterminal" / "Images"


def detect_base_color(img):
    """Detect the dominant base color by sampling corners + most common pixel."""
    w, h = img.size
    # The base color is extremely dominant (88-96%), so corner pixel is reliable
    # and much faster than counting all pixels
    base = img.getpixel((0, 0))
    return base


def darken_color(rgb, target_brightness):
    """Darken an RGB color to target_brightness while preserving hue/saturation."""
    r, g, b = rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    new_l = l * target_brightness / max(l, 0.01)  # scale lightness down
    new_l = min(new_l, target_brightness)
    nr, ng, nb = colorsys.hls_to_rgb(h, new_l, s)
    return (int(nr * 255), int(ng * 255), int(nb * 255))


def process_image(filepath, target_brightness, dry_run=False):
    """Detect base color, build a color remap, and darken the image."""
    img = Image.open(filepath).convert("RGB")
    base = detect_base_color(img)
    dark_base = darken_color(base, target_brightness)

    if dry_run:
        print(f"  {filepath.name}: base={base} -> dark={dark_base}")
        return None

    # Convert to work with raw pixel data for speed
    pixels = img.load()
    w, h = img.size

    # Precompute: how "close" is each pixel to the base color?
    # Pixels close to base get shifted toward dark_base.
    # Pixels far from base (detail colors) get darkened proportionally
    # but keep their relative contrast to the base.
    br, bg, bb = base
    dr, dg, db = dark_base

    # Scale factor: ratio of dark_base brightness to original base brightness
    orig_lum = (0.299 * br + 0.587 * bg + 0.114 * bb)
    dark_lum = (0.299 * dr + 0.587 * dg + 0.114 * db)
    if orig_lum < 1:
        orig_lum = 1
    scale = dark_lum / orig_lum

    for y in range(h):
        for x in range(w):
            r, g, b = pixels[x, y]
            # Distance from base color
            dist = abs(r - br) + abs(g - bg) + abs(b - bb)

            if dist < 30:
                # Very close to base color -> map directly to dark base
                # Blend based on how close: dist=0 -> full dark_base, dist=30 -> transition
                t = dist / 30.0
                nr = int(dr * (1 - t) + (r * scale) * t)
                ng = int(dg * (1 - t) + (g * scale) * t)
                nb = int(db * (1 - t) + (b * scale) * t)
            else:
                # Detail pixel: scale brightness down but preserve relative color
                # Keep the color difference from base, but in the dark palette
                diff_r = r - br
                diff_g = g - bg
                diff_b = b - bb
                # Apply the diff on top of the dark base, slightly amplified for visibility
                amp = 1.3  # amplify details slightly so they pop on dark background
                nr = int(max(0, min(255, dr + diff_r * amp)))
                ng = int(max(0, min(255, dg + diff_g * amp)))
                nb = int(max(0, min(255, db + diff_b * amp)))

            pixels[x, y] = (max(0, min(255, nr)),
                            max(0, min(255, ng)),
                            max(0, min(255, nb)))

    return img


def main():
    parser = argparse.ArgumentParser(description="Darken Pokemon terminal images")
    parser.add_argument("--target-brightness", type=float, default=0.15,
                        help="Target brightness for base color (0.0-1.0, default: 0.15)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print changes without modifying files")
    parser.add_argument("--preview", type=str, default=None,
                        help="Process only this single file and save as *_dark.jpg")
    parser.add_argument("--backup", action="store_true",
                        help="Backup originals to Images_backup/ before modifying")
    args = parser.parse_args()

    if args.preview:
        filepath = Path(args.preview)
        if not filepath.exists():
            print(f"File not found: {filepath}")
            sys.exit(1)
        print(f"Processing preview: {filepath}")
        img = process_image(filepath, args.target_brightness)
        if img:
            out = filepath.with_stem(filepath.stem + "_dark")
            img.save(out, "JPEG", quality=90)
            print(f"Saved: {out}")
        return

    if not IMAGES_DIR.exists():
        print(f"Images directory not found: {IMAGES_DIR}")
        sys.exit(1)

    if args.backup and not args.dry_run:
        backup_dir = IMAGES_DIR.parent / "Images_backup"
        if not backup_dir.exists():
            print(f"Creating backup at {backup_dir} ...")
            shutil.copytree(IMAGES_DIR, backup_dir)
            print("Backup complete.")
        else:
            print(f"Backup already exists at {backup_dir}, skipping.")

    jpg_files = sorted(IMAGES_DIR.rglob("*.jpg"))
    total = len(jpg_files)
    print(f"Found {total} images. Target brightness: {args.target_brightness}")

    for i, filepath in enumerate(jpg_files, 1):
        rel = filepath.relative_to(IMAGES_DIR)
        print(f"[{i}/{total}] {rel}", end="")
        if args.dry_run:
            process_image(filepath, args.target_brightness, dry_run=True)
        else:
            img = process_image(filepath, args.target_brightness)
            if img:
                img.save(filepath, "JPEG", quality=90)
                print(" ... done")
            else:
                print(" ... skipped")

    print(f"\nFinished processing {total} images.")


if __name__ == "__main__":
    main()
