from pathlib import Path
from playwright.sync_api import sync_playwright

path = (Path(__file__).resolve().parents[1] / "dist" / "index.html").as_uri()
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 390, "height": 844})
    page.goto(path)
    summary = page.locator("#radio-summary").inner_text().lower()
    print("Radio summary on mobile:", repr(summary), flush=True)
    assert "1265 matching radio records" in summary.replace(",", "").lower(), summary
    page.locator("#radio-q").fill("Noa Kushner")
    assert "1 matching radio record" in page.locator("#radio-summary").inner_text().lower()
    assert not page.locator("#radio-more").is_visible(), "Unexpected radio Show more"
    ink = page.locator("#radio-results h3").first.evaluate("(el) => getComputedStyle(el).color")
    assert ink == "rgb(244, 240, 230)", ink
    page.locator("#writing-q").fill("Finding Gratitude")
    assert "2 matching source records" in page.locator("#writing-summary").inner_text().lower()
    assert not page.locator("#writing-more").is_visible(), "Unexpected writing Show more"
    outputs = Path(__file__).resolve().parents[1] / "artifacts" / "browser-review"
    outputs.mkdir(parents=True, exist_ok=True)
    page.locator("#radio-browser").screenshot(path=str(outputs / "mobile-radio.png"))
    page.locator("#writing-browser").screenshot(path=str(outputs / "mobile-writing.png"))
    page.set_viewport_size({"width": 1280, "height": 800})
    y_search = page.locator("#radio-q").bounding_box()["y"]
    y_status = page.locator("#radio-state").bounding_box()["y"]
    assert abs(y_search - y_status) < 3, "Desktop radio filters do not fit one row"
    page.locator("#radio-browser").screenshot(path=str(outputs / "desktop-radio.png"))
    browser.close()
