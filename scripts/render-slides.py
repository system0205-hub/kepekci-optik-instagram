"""
Claude Design HTML'inden her slide'i 1080x1350 PNG olarak kaydeder.
Instagram carousel icin hazir dosyalar uretir.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

# CLI: python render-slides.py <klasor> [name1,name2,...]
FOLDER = Path(sys.argv[1] if len(sys.argv) > 1 else r"c:\Users\Edu\Desktop\Claude yapılan uygulamalar\Ai ile İnstagram\exports\progresif-cam-nedir").resolve()
HTML = FOLDER / "design-source.html"
OUT = FOLDER
url = "file:///" + str(HTML).replace("\\", "/")

# Isteğe bağlı slide isimleri
_names_arg = sys.argv[2] if len(sys.argv) > 2 else "01,02,03,04,05"
_names = _names_arg.split(",")
SLIDE_NAMES = {i+1: n.strip() for i, n in enumerate(_names)}

print(f"Rendering: {HTML.name}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(
        viewport={"width": 1080, "height": 1350},
        device_scale_factor=2,  # retina kalite
    )
    page = ctx.new_page()
    page.goto(url, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(6000)  # JS unpack icin bekle

    # Her slide'i bul, scroll et (JS nav state update), sonra screenshot al
    for i in range(1, 6):
        selector = f"section.slide.s{i}"
        try:
            page.wait_for_selector(selector, timeout=5000)
            element = page.locator(selector).first
            # Kritik: scroll ile IntersectionObserver tetiklenir, nav dot aktif olur
            element.scroll_into_view_if_needed()
            page.wait_for_timeout(800)  # JS state update icin bekle
            out_path = OUT / f"{SLIDE_NAMES[i]}.png"
            element.screenshot(path=str(out_path))
            size_kb = out_path.stat().st_size // 1024
            print(f"  OK s{i} -> {out_path.name} ({size_kb} KB)")
        except Exception as e:
            print(f"  FAIL s{i}: {e}")

    browser.close()

print("\nDone. Files:")
for f in sorted(OUT.glob("*.png")):
    print(f"  {f.name}")
