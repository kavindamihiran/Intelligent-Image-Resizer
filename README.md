# Image Resizer - Advanced Python Tool

A powerful Python script for resizing images with two distinct modes:

## Features

### 🎯 **Size Mode**

- Resize images to achieve a specific file size (e.g., 500KB, 1.5MB)
- Maintains original pixel dimensions and aspect ratio
- Uses intelligent quality adjustment to reach target size
- Supports JPEG and WebP formats
- Preserves or strips metadata as needed

### 📐 **DPI Mode**

- **NEW:** Automatically adjust DPI to reach target file size
- Option to use fixed DPI with quality adjustment
- Perfect for print preparation while controlling file size
- Maintains same visual appearance and pixel count
- Supports JPEG, PNG, WebP, and TIFF formats
- Intelligent DPI optimization for target size

## Installation

### Requirements

- Python 3.7 or higher
- Pillow (PIL) library

### Install Dependencies

```bash
# Required
pip install Pillow

# Optional (for progress bars)
pip install tqdm
```

## Usage

### Size Mode Examples

**Resize single image to 500KB:**

```bash
python image_resizer_improved.py size -i photo.jpg -o resized.jpg -t 500KB
```

**Batch resize directory to 1MB each:**

```bash
python image_resizer_improved.py size -i photos/ -d output/ -t 1MB --ext .webp
```

**Resize with metadata preservation:**

```bash
python image_resizer_improved.py size -i photo.jpg -o output.jpg -t 200KB --keep-metadata
```

### DPI Mode Examples

**Resize to 200KB by auto-adjusting DPI:**

```bash
python image_resizer_improved.py dpi -i scan.jpg -o output.jpg -t 200KB
```

**Resize to 1MB with fixed DPI:**

```bash
python image_resizer_improved.py dpi -i scan.jpg -o output.jpg -t 1MB --fixed-dpi 300
```

**Batch resize with auto-DPI adjustment:**

```bash
python image_resizer_improved.py dpi -i photos/ -d output/ -t 800KB
```

**Batch resize with fixed DPI:**

```bash
python image_resizer_improved.py dpi -i scanned_docs/ -d output/ -t 500KB --fixed-dpi 150
```

## Supported Formats

### Size Mode

- **Input:** JPEG, PNG, TIFF, WebP (most formats)
- **Output:** JPEG (.jpg, .jpeg), WebP (.webp)

### DPI Mode

- **Input/Output:** JPEG (.jpg, .jpeg), PNG (.png), WebP (.webp), TIFF (.tiff, .tif)

## Advanced Options

| Option            | Description                              |
| ----------------- | ---------------------------------------- |
| `--keep-metadata` | Preserve EXIF and other metadata         |
| `--ext .webp`     | Force output format for batch processing |
| `--no-progress`   | Disable progress bars                    |
| `-v, --verbose`   | Show detailed results                    |

## Size Format Examples

The size parser accepts various human-readable formats:

- `500KB` or `500k` = 512,000 bytes
- `1.5MB` or `1.5m` = 1,572,864 bytes
- `2GB` or `2g` = 2,147,483,648 bytes
- `100000` = 100,000 bytes (raw number)

## How It Works

### Size Mode Algorithm

1. **Binary Search:** Uses binary search to find optimal quality setting
2. **Smart Compression:** Adjusts JPEG/WebP quality to reach target size
3. **Tolerance:** Accepts results within 5% of target size
4. **Fallback:** If target unreachable, saves at lowest quality

### DPI Mode Process

1. **Metadata Update:** Changes DPI information in image headers
2. **No Resampling:** Preserves exact pixel data
3. **Format Optimization:** Uses best compression for each format

## Error Handling

The script provides comprehensive error handling:

- Invalid file formats
- Corrupted images
- Insufficient permissions
- Unreachable target sizes
- Missing dependencies

## Performance

- **Memory Efficient:** Processes images one at a time
- **Fast Binary Search:** Typically finds optimal quality in 5-10 iterations
- **Batch Processing:** Progress bars and status updates
- **Large Image Support:** No pixel limits (configurable)

## Examples with Real Use Cases

### Web Optimization

```bash
# Optimize images for web (under 200KB each)
python image_resizer_improved.py size -i website_images/ -d optimized/ -t 200KB --ext .webp
```

### Print Preparation

```bash
# Set high DPI for printing
python image_resizer_improved.py dpi -i photos/ -d print_ready/ --dpi 300 --keep-metadata
```

### Email Attachments

```bash
# Reduce file size for email
python image_resizer_improved.py size -i vacation_photos/ -d email_sized/ -t 500KB
```

## Troubleshooting

**Import Error (tqdm):** The script works without tqdm, just without fancy progress bars.

**Large Files:** For very large images, increase system memory or use smaller target sizes.

**Quality Issues:** Size mode may reduce quality significantly for very small target sizes.

**Format Support:** Check that your output format supports the features you need (e.g., DPI support).

## License

This script is provided as-is for educational and practical use.
