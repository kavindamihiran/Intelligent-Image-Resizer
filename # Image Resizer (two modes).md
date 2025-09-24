# Image Resizer (two modes)

Install
- python -m venv .venv && source .venv/bin/activate
- pip install -r requirements.txt

Modes
1) size: Keep pixel resolution the same, adjust compression to reach a target file size (JPEG/WebP).
2) dpi: Keep pixel resolution the same, change pixel density (DPI metadata).

Examples
- Single file to ~300KB (keeps pixels, adjusts quality):
  python resize_images.py size -i input.jpg -o output.jpg -t 300KB

- Batch folder to ~500KB each, output as WebP:
  python resize_images.py size -i ./photos -t 500KB --ext .webp

- Set DPI to 300 without changing pixels:
  python resize_images.py dpi -i input.png -o output.png --dpi 300

Notes
- Size mode supports .jpg/.jpeg/.webp as outputs.
- If lowest quality still can't hit target, the script saves best-effort and reports failure.
- DPI changes physical print size; file size may remain similar. 
