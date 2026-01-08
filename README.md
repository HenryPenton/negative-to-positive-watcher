# Film Negative to Positive Converter

A Docker container that watches a folder for image files and automatically converts them to positives by inverting the colors. Supports TIFF, JPEG, PNG, BMP, GIF, and WebP formats.

## Features

- 📁 Automatic folder monitoring
- 🖼️ Multiple format support (TIFF, JPEG, PNG, BMP, GIF, WebP)
- 🔄 Converts negatives to positives via image inversion
- 🎨 Handles RGB, RGBA, grayscale, and 16-bit images
- 📦 Easy Docker Compose setup
- 🔁 Configurable polling interval

## Quick Start with Docker Compose

The easiest way to run the converter is using Docker Compose:

```bash
docker compose up -d
```

This will:
- Build the container
- Mount `./negatives` as the watch directory
- Mount `./positives` as the output directory
- Start watching for new images

## Manual Docker Build & Run

### Build

```bash
docker build -t negative-to-positive .
```

### Run

```bash
docker run -d \
  --name negative-converter \
  -v /path/to/your/negatives:/watch \
  -v /path/to/output:/output \
  negative-to-positive
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `WATCH_DIR` | `/watch` | Directory to watch for new image files |
| `OUTPUT_DIR` | `/output` | Directory to save converted positives |
| `POLL_INTERVAL` | `60` | Seconds between directory scans |

## Example with Custom Settings

```bash
docker run -d \
  --name negative-converter \
  -v ~/film-scans/negatives:/watch \
  -v ~/film-scans/positives:/output \
  -e POLL_INTERVAL=10 \
  negative-to-positive
```

## Supported Formats

- TIFF (`.tif`, `.tiff`)
- JPEG (`.jpg`, `.jpeg`)
- PNG (`.png`)
- BMP (`.bmp`)
- GIF (`.gif`)
- WebP (`.webp`)

All output files are saved as TIFF with LZW compression for quality preservation.

## How It Works

1. The container watches the specified directory for new image files
2. When a new image is detected, it inverts the colors (negative → positive)
3. The converted image is saved to the output directory with `_positive.tif` appended to the filename
4. Original files are not modified and remain in the watch directory
5. Each file is processed only once (tracked to avoid reprocessing)

## Usage

1. Place your negative images in the `negatives/` folder
2. Converted positive images will appear in the `positives/` folder
3. Monitor progress with `docker compose logs -f`

## View Logs

```bash
# Docker Compose
docker compose logs -f

# Docker
docker logs -f negative-converter
```

## Stop

```bash
# Docker Compose
docker compose down

# Docker
docker stop negative-converter
docker rm negative-converter
```

## Development

The project uses Python with Pillow (PIL) for image processing. To run locally without Docker:

```bash
pip install Pillow
export WATCH_DIR="./negatives"
export OUTPUT_DIR="./positives"
export POLL_INTERVAL="60"
python watcher.py
```

## License

See [LICENSE](LICENSE) file for details.
