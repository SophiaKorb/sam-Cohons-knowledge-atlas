from pathlib import Path
from playwright.sync_api import sync_playwright

path = (Path(__file__).resolve().parents[1] / "dist" / "index.html").as_uri()
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 390, "height": 844})
    page.goto(path)
    assert "1,263 matching radio records" in page.locator("#radio-summary").inner_text()
    page.locator("#radio-q").fill("Noa Kushner")
    assert "1 matching radio record" in page.locator("#radio-summary").inner_text()
    page.locator("#writing-q").fill("Finding Gratitude")
    assert "2 matching source records" in page.locator("#writing-summary").inner_text()
    browser.close()
