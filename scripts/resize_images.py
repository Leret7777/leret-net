#!/usr/bin/env python3
"""
resize_images.py — shrink raw photos before they go into the repo.

This is the ONE script in the whole project that uses an external
library (Pillow, for image processing) instead of just the standard
library. Install it once with:

    pip install Pillow

Usage:
    python3 scripts/resize_images.py incoming/portrait src/images/modeling/portrait

Every image in the source folder is resized so its longest edge is at
most MAX_DIMENSION pixels, re-saved as a compressed JPEG, and written
into the destination folder — same filename, but with a .jpg extension.
Raw camera photos are often 4000px+ wide and several MB each; this
script gets them down to something reasonable for a website (a few
hundred KB, plenty sharp on screen) so the git repo doesn't balloon in
size every time you add a shoot.

incoming/ is listed in .gitignore on purpose — it's meant to hold your
untouched, full-size originals so they never get committed. Run this
script to process them into src/images/, and only what comes OUT of
this script gets committed.
"""

import os
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit(
        "Pillow isn't installed. Run: pip install Pillow\n"
        "(This is the only script in the project that needs it.)"
    )

MAX_DIMENSION = 1600  # longest edge, in pixels
JPEG_QUALITY = 82  # 0-100; 82 is a good balance of size vs. quality

VALID_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".heic", ".tif", ".tiff")


def resize_one(src_path, dest_path):
    with Image.open(src_path) as img:
        # Photos taken on a phone often carry an EXIF "orientation" tag
        # instead of actually being rotated — ImageOps.exif_transpose
        # bakes that rotation into the pixels so it displays correctly
        # everywhere, including browsers that ignore EXIF.
        from PIL import ImageOps

        img = ImageOps.exif_transpose(img)

        # JPEG has no transparency channel, so flatten anything with one
        # (PNG, WEBP with alpha) onto a white background before saving.
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        width, height = img.size
        longest_edge = max(width, height)
        if longest_edge > MAX_DIMENSION:
            scale = MAX_DIMENSION / longest_edge
            new_size = (round(width * scale), round(height * scale))
            # LANCZOS is a high-quality resampling filter — slower than
            # the default but noticeably sharper for photos.
            img = img.resize(new_size, Image.LANCZOS)

        img.save(dest_path, "JPEG", quality=JPEG_QUALITY, optimize=True)


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python3 scripts/resize_images.py <source_folder> <dest_folder>")

    src_dir, dest_dir = sys.argv[1], sys.argv[2]

    if not os.path.isdir(src_dir):
        sys.exit(f"Source folder not found: {src_dir}")

    os.makedirs(dest_dir, exist_ok=True)

    processed = 0
    for filename in sorted(os.listdir(src_dir)):
        if not filename.lower().endswith(VALID_EXTENSIONS):
            continue

        src_path = os.path.join(src_dir, filename)
        name_without_ext = os.path.splitext(filename)[0]
        dest_path = os.path.join(dest_dir, name_without_ext + ".jpg")

        resize_one(src_path, dest_path)
        before_kb = os.path.getsize(src_path) / 1024
        after_kb = os.path.getsize(dest_path) / 1024
        print(f"  {filename} -> {os.path.basename(dest_path)}  ({before_kb:.0f}KB -> {after_kb:.0f}KB)")
        processed += 1

    print(f"\nDone. Processed {processed} image(s) into {dest_dir}")


if __name__ == "__main__":
    main()
