from playwright.sync_api import sync_playwright
import json

def get_trends(country="worldwide", date="29-11-2024", ztime="Europe/Madrid"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        url = f"https://archive.twitter-trending.com/{country}/{date}"
        page.goto(url)
        
        page.wait_for_timeout(3000)  # espera que es generi 'q'
        q = page.evaluate("window.tghjy")  # comprova el nom correcte
        
        # Fem el POST i guardem el text immediatament
        response = page.request.post(
            "https://archive.twitter-trending.com/tablo_request.php",
            data={
                "country": country,
                "date": date,
                "ztime": ztime,
                "q": q
            }
        )
        text_response = response.text()  # llegim abans de tancar
        
        browser.close()
        
        try:
            return json.loads(text_response)
        except json.JSONDecodeError:
            return text_response

if __name__ == "__main__":
    trends = get_trends()
    print(json.dumps(trends, indent=2, ensure_ascii=False))
