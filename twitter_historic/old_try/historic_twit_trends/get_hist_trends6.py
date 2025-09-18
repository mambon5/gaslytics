from playwright.sync_api import sync_playwright
import json

pais = "worldwide"
data = "29-11-2024"
ztime = "Europe/Madrid"

url = f"https://archive.twitter-trending.com/{pais}/{data}"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    captured = {"request": None, "response": None}

    def on_request(request):
        if "tablo_request.php" in request.url and request.method == "POST":
            print("✅ POST detectat!")
            print("Payload:", request.post_data)
            captured["request"] = request

    def on_response(response):
        if "tablo_request.php" in response.url:
            captured["response"] = response

    page.on("request", on_request)
    page.on("response", on_response)

    page.goto(url)
    page.wait_for_timeout(5000)

    if captured["request"] and captured["response"]:
        text = captured["response"].text()
        print("\n--- INFO COMPLETA ---")
        print("URL:", captured["request"].url)
        print("POST data:", captured["request"].post_data)
        print("Resposta JSON (truncada):", text[:300], "...")

        # Guardem la resposta sencera en un fitxer
        with open("trends.json", "w", encoding="utf-8") as f:
            f.write(text)
        print("📁 Resposta guardada a trends.json")
    else:
        print("⚠️ No s’ha detectat ni request ni response a tablo_request.php")

    browser.close()

