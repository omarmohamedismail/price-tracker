from playwright.sync_api import sync_playwright
import requests
import os

MAX_RESULTS = 10
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    response = requests.post(url, data={"chat_id": CHAT_ID, "text": text})
    print("رد تليجرام:", response.status_code, response.text)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://books.toscrape.com/")
    
    page.wait_for_timeout(2000)
    
    print("عنوان الصفحة:", page.title())
    
    books = page.locator("article.product_pod")
    count = books.count()
    print("عدد الكتب:", count)
    
    results = []
    
    for i in range(min(count, MAX_RESULTS)):
        book = books.nth(i)
        try:
            name = book.locator("h3 a").get_attribute("title")
            price = book.locator(".price_color").inner_text()
            
            results.append(f"{name}\nالسعر: {price}")
            print(f"{i+1}. {name} - {price}")
        except Exception as e:
            print(f"كتاب رقم {i+1} اتخطى، السبب:", e)
            continue
    
    if results:
        message = "📚 قائمة الكتب والأسعار:\n\n" + "\n\n".join(results)
        send_telegram_message(message)
    else:
        print("مفيش نتائج اتقرت")
    
    browser.close()