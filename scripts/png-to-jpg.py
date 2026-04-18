"""PNG'leri Instagram icin JPG'ye cevir (max 2MB, kalite 92)."""
import sys
from pathlib import Path
from PIL import Image

folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
print(f"Folder: {folder}")

for png in sorted(folder.glob("*.png")):
    if png.name.startswith("_"):  # discovery vb. skip
        continue
    jpg = png.with_suffix(".jpg")
    img = Image.open(png).convert("RGB")
    # Instagram carousel: 1080x1350
    if img.size != (1080, 1350):
        print(f"  resize {png.name}: {img.size} -> 1080x1350")
        img = img.resize((1080, 1350), Image.LANCZOS)
    img.save(jpg, "JPEG", quality=92, optimize=True)
    print(f"  {png.name} -> {jpg.name} ({jpg.stat().st_size // 1024} KB)")
