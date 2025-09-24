# Image Resizer - Intelligent Image Resizing Tool

A powerful Python tool for **resizing images to achieve target file sizes**. Simply specify your desired file size (e.g., 500KB, 1.5MB) and let the tool automatically resize your images to match that target.

The tool offers **two processing modes** as sub-features to handle different image types optimally:

## Main Feature

**🎯 Resize Images to Target File Size** - The core functionality that automatically adjusts your images to match your specified file size target.

## Processing Modes (Sub-features)

### **Size Mode**

- Uses intelligent quality adjustment to reach target file size
- Maintains original pixel dimensions and aspect ratio
- Best for JPEG and WebP formats
- Preserves or strips metadata as needed

### **DPI Mode**

- Uses DPI adjustment to reach target file size
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

### Basic Usage (Default Behavior)

**Resize single image to 500KB (creates photo_resized.jpg):**

```bash
python main.py size photo.jpg 500KB
```

**Resize to 2MB using DPI mode (creates photo_resized.jpg):**

```bash
python main.py dpi photo.jpg 2MB
```

### Size Mode Examples

**Resize single image to 500KB:**

```bash
python main.py size photo.jpg 500KB
```

**Replace original file (overwrite):**

```bash
python main.py size photo.jpg 500KB --overwrite
```

**Batch resize directory to 1MB each:**

```bash
python main.py size photos/ 1MB --output output/
```

**Resize with custom suffix:**

```bash
python main.py size photo.jpg 200KB --suffix _web
```

### DPI Mode Examples

**Resize to 200KB by adjusting DPI:**

```bash
python main.py dpi scan.jpg 200KB
```

**Resize to 1MB with output directory:**

```bash
python main.py dpi scan.jpg 1MB --output resized/
```

**Batch resize with DPI adjustment:**

```bash
python main.py dpi photos/ 800KB --output output/
```

**Batch resize with suffix:**

```bash
python main.py dpi scanned_docs/ 500KB --suffix _optimized
```

## Supported Formats

### Size Mode

- **Input:** JPEG, PNG, TIFF, WebP (most formats)
- **Output:** JPEG (.jpg, .jpeg), WebP (.webp)

### DPI Mode

- **Input/Output:** JPEG (.jpg, .jpeg), PNG (.png), WebP (.webp), TIFF (.tiff, .tif)

## Advanced Options

| Option                | Description                           |
| --------------------- | ------------------------------------- |
| `--output`, `-o`      | Output directory for processed images |
| `--suffix`            | Add suffix to output filenames        |
| `--overwrite`         | Overwrite existing output files       |
| `--no-auto-increment` | Disable automatic filename increment  |
| `--no-progress`       | Disable progress bars                 |
| `--verbose`, `-v`     | Show detailed results                 |

### Auto-Increment Feature

By default, the tool automatically prevents file overwrites by adding numeric suffixes:

- First run: `image.jpg` → `image_resized.jpg`
- Second run: `image.jpg` → `image_resized_1.jpg`
- Third run: `image.jpg` → `image_resized_2.jpg`
- And so on...

**Examples:**

```bash
# Multiple runs create unique files automatically
python main.py size photo.jpg 500KB
python main.py size photo.jpg 400KB  # Creates photo_resized_1.jpg
python main.py size photo.jpg 300KB  # Creates photo_resized_2.jpg

# Works with custom suffixes too
python main.py size photo.jpg 500KB --suffix _web
python main.py size photo.jpg 400KB --suffix _web  # Creates photo_web_1.jpg

# Disable auto-increment to force overwrite
python main.py size photo.jpg 500KB --no-auto-increment
```

**Benefits:**

- ✅ Never accidentally overwrite existing files
- ✅ Unlimited resize attempts on same image
- ✅ Perfect for experimenting with different target sizes
- ✅ Maintains history of all resize operations

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
python main.py size website_images/ 200KB --output optimized/ --verbose
```

### Print Preparation

```bash
# Resize images for print while controlling file size
python main.py dpi photos/ 2MB --output print_ready/ --suffix _print
```

### Email Attachments

```bash
# Reduce file size for email
python main.py size vacation_photos/ 500KB --output email_sized/
```

### Batch Processing with Progress

```bash
# Process many images with progress tracking
python main.py size *.jpg 1MB --suffix _web --verbose
```

## Troubleshooting

**Import Error (tqdm):** The script works without tqdm, just without fancy progress bars.

**Large Files:** For very large images, increase system memory or use smaller target sizes.

**Quality Issues:** Size mode may reduce quality significantly for very small target sizes.

**Format Support:** Check that your output format supports the features you need (e.g., DPI support).

## License

This script is provided as-is for educational and practical use.
