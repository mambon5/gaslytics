from playwright.sync_api import sync_playwright

pais = "worldwide"
data = "29-11-2024"
ztime = "Europe/Madrid"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Interceptem el POST a tablo_request.php
    def handle_request(route, request):
        if "tablo_request.php" in request.url and request.method == "POST":
            print("POST detectat!")
            print("Payload:", request.post_data)
        route.continue_()

    page.route("**/*", handle_request)
    page.goto(f"https://archive.twitter-trending.com/{pais}/{data}")
    page.wait_for_timeout(3000)
    
    browser.close()
