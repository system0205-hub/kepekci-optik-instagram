"""
Claude Design HTML'ini aç, yapisini kesfet.
Tek scrollable mi, slide navigation mi, grid mi?
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HTML = Path(r"c:\Users\Edu\Desktop\Claude yapılan uygulamalar\Ai ile İnstagram\exports\progresif-cam-nedir\design.html").resolve()
OUT = HTML.parent / "_discovery"
OUT.mkdir(exist_ok=True)

url = "file:///" + str(HTML).replace("\\", "/")
print("Opening:", url)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1080, "height": 1350}, device_scale_factor=2)
    page = ctx.new_page()
    page.goto(url, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(5000)  # JS unpack bekle

    # Tam sayfa screenshot
    page.screenshot(path=str(OUT / "full-page.png"), full_page=True)
    print("Full page screenshot saved")

    # Yapi analizi
    info = page.evaluate("""
    () => {
        const body = document.body;
        const html = document.documentElement;
        const slides = document.querySelectorAll('[class*="slide"], [data-slide], section, .page, .frame');
        const result = {
            docWidth: html.scrollWidth,
            docHeight: html.scrollHeight,
            viewportWidth: window.innerWidth,
            viewportHeight: window.innerHeight,
            slideCount: slides.length,
            slideSelectors: Array.from(slides).slice(0, 10).map(el => ({
                tag: el.tagName,
                cls: el.className,
                id: el.id,
                w: el.offsetWidth,
                h: el.offsetHeight,
                x: el.offsetLeft,
                y: el.offsetTop
            })),
            bodyChildren: Array.from(body.children).slice(0, 5).map(el => ({
                tag: el.tagName,
                cls: el.className,
                id: el.id,
                w: el.offsetWidth,
                h: el.offsetHeight
            }))
        };
        return result;
    }
    """)
    import json
    print(json.dumps(info, indent=2, ensure_ascii=False))

    browser.close()
