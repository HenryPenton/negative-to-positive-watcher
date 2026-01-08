#!/usr/bin/env python3
"""
Film Negative to Positive Converter
Watches a folder for image files and inverts them to convert negatives to positives.
"""

import os
import time
import logging
from pathlib import Path

from PIL import Image, ImageOps

# Supported image extensions
SUPPORTED_EXTENSIONS = (
    ".tif",
    ".tiff",  # TIFF
    ".jpg",
    ".jpeg",  # JPEG
    ".png",  # PNG
    ".bmp",  # Bitmap
    ".gif",  # GIF
    ".webp",  # WebP
)

# Configuration
WATCH_DIR = os.environ.get("WATCH_DIR", "/watch")
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "/output")
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "60"))
PROCESSED_SUFFIX = "_positive"

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Track processed files
processed_files = set()


def is_supported(filename):
    """Check if file is a supported image format."""
    return filename.lower().endswith(SUPPORTED_EXTENSIONS)


def invert_image(input_path, output_path):
    """Invert a TIFF image (negative to positive conversion)."""
    try:
        with Image.open(input_path) as img:
            # Handle different image modes
            if img.mode == "RGBA":
                # Separate alpha channel, invert RGB, recombine
                r, g, b, a = img.split()
                rgb = Image.merge("RGB", (r, g, b))
                inverted_rgb = ImageOps.invert(rgb)
                r2, g2, b2 = inverted_rgb.split()
                inverted = Image.merge("RGBA", (r2, g2, b2, a))
            elif img.mode in ("RGB", "L"):
                inverted = ImageOps.invert(img)
            elif img.mode == "I;16":
                # 16-bit grayscale - convert, invert, save
                img_8bit = img.point(lambda x: x / 256).convert("L")
                inverted = ImageOps.invert(img_8bit)
            else:
                # Convert to RGB first if needed
                converted = img.convert("RGB")
                inverted = ImageOps.invert(converted)

            # Preserve TIFF metadata if possible
            inverted.save(output_path, format="TIFF", compression="lzw")
            logger.info(f"Successfully converted: {input_path} -> {output_path}")
            return True

    except Exception as e:
        logger.error(f"Failed to process {input_path}: {e}")
        return False


def get_output_filename(input_filename):
    """Generate output filename with _positive suffix (outputs as TIFF for quality)."""
    path = Path(input_filename)
    return f"{path.stem}{PROCESSED_SUFFIX}.tif"


def process_new_files():
    """Scan watch directory and process new TIFF files."""
    watch_path = Path(WATCH_DIR)
    output_path = Path(OUTPUT_DIR)

    if not watch_path.exists():
        logger.warning(f"Watch directory does not exist: {WATCH_DIR}")
        return

    # Ensure output directory exists
    output_path.mkdir(parents=True, exist_ok=True)

    for file_path in watch_path.iterdir():
        if file_path.is_file() and is_supported(file_path.name):
            file_key = str(file_path)

            # Skip already processed files
            if file_key in processed_files:
                continue

            # Skip files that are still being written (check if size is stable)
            try:
                size1 = file_path.stat().st_size
                time.sleep(0.5)
                size2 = file_path.stat().st_size
                if size1 != size2:
                    logger.debug(f"File still being written: {file_path.name}")
                    continue
            except OSError:
                continue

            logger.info(f"Found new image: {file_path.name}")

            output_filename = get_output_filename(file_path.name)
            output_file = output_path / output_filename

            if invert_image(str(file_path), str(output_file)):
                processed_files.add(file_key)


def main():
    """Main watch loop."""
    logger.info("=" * 50)
    logger.info("Film Negative to Positive Converter")
    logger.info("=" * 50)
    logger.info(f"Watching directory: {WATCH_DIR}")
    logger.info(f"Output directory: {OUTPUT_DIR}")
    logger.info(f"Poll interval: {POLL_INTERVAL} seconds")
    logger.info("=" * 50)

    # Create directories if they don't exist
    Path(WATCH_DIR).mkdir(parents=True, exist_ok=True)
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    while True:
        try:
            process_new_files()
        except Exception as e:
            logger.error(f"Error in processing loop: {e}")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
