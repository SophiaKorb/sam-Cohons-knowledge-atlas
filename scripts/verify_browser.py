from pathlib import Path
from playwright.sync_api import sync_playwright

path = (Path(__file__).resolve().parents[1] / "dist" / "index.html").as_uri()
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 390, "height": 844})
    page.goto(path)
    summary = page.locator("#radio-summary").inner_text().lower()
    print("Radio summary on mobile:", repr(summary), flush=True)
    assert "1263 matching radio records" in summary.replace(",", "").lower(), summary
    page.locator("#radio-q").fill("Noa Kushner")
    assert "1 matching radio record" in page.locator("#radio-summary").inner_text().lower()
    ink = page.locator("#radio-results h3").first.evaluate("(el) => getComputedStyle(el).color")
    assert ink == "rgb(244, 240, 230)", ink
    page.locator("#writing-q").fill("Finding Gratitude")
    assert "2 matching source records" in page.locator("#writing-summary").inner_text().lower()
    outputs = Path(__file__).resolve().parents[1] / "artifacts" / "browser-review"
    outputs.mkdir(parents=True, exist_ok=True)
    page.locator("#radio-browser").screenshot(path=str(outputs / "mobile-radio.png"))
    page.locator("#writing-browser").screenshot(path=str(outputs / "mobile-writing.png"))
    page.set_viewport_size({"width": 1280, "height": 800})
    page.locator("#radio-browser").screenshot(path=str(outputs / "desktop-radio.png"))
    browser.close()
