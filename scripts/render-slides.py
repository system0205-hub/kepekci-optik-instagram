"""
Claude Design HTML'inden her slide'i 1080x1350 PNG olarak kaydeder.
Instagram carousel icin hazir dosyalar uretir.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

HTML = Path(r"c:\Users\Edu\Desktop\Claude yapılan uygulamalar\Ai ile İnstagram\exports\progresif-cam-nedir\design-source.html").resolve()
OUT = HTML.parent
url = "file:///" + str(HTML).replace("\\", "/")

SLIDE_NAMES = {
    1: "01-kapak",
    2: "02-nedir",
    3: "03-kimler-kullanmali",
    4: "04-avantajlari",
    5: "05-iletisim",
}

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

    # Her slide'i bul ve screenshot al
    for i in range(1, 6):
        selector = f"section.slide.s{i}"
        try:
            page.wait_for_selector(selector, timeout=5000)
            element = page.locator(selector).first
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
