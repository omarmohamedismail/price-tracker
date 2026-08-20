from playwright.sync_api import sync_playwright
import re
import requests

TARGET_PRICE = 99999  # سيبها كده مؤقتاً للتجربة، بعد كده رجعها 5100
TELEGRAM_TOKEN = "8747840328:AAG8YWIodfk9CyCIRv7n1yotPg1lCkPAbpA"
CHAT_ID = "5241219849"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    response = requests.post(url, data={"chat_id": CHAT_ID, "text": text})
    print("رد تليجرام:", response.status_code, response.text)

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        executable_path=r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
    )
    page = browser.new_page()
    page.goto("https://a.co/d/0gEox93f")
    
    page.wait_for_timeout(3000)
    
    print("عنوان المنتج:", page.title())
    
    try:
        price_whole = re.sub(r"[^\d,]", "", page.locator(".a-price-whole").first.inner_text())
        price_fraction = re.sub(r"[^\d]", "", page.locator(".a-price-fraction").first.inner_text())
        
        current_price = float(price_whole.replace(",", "") + "." + price_fraction)
        
        print("السعر الحالي:", current_price)
        print("السعر المستهدف:", TARGET_PRICE)
        
        if current_price <= TARGET_PRICE:
            message = f"🎉 السعر نزل!\nالسعر الحالي: {current_price}\nالرابط: https://a.co/d/0gEox93f"
            send_telegram_message(message)
        else:
            print("لسه السعر أعلى من اللي انت عايزه، هنراقب.")
            
    except Exception as e:
        print("معرفتش أقرا السعر، السبب:", e)
    
    page.wait_for_timeout(5000)
    browser.close()