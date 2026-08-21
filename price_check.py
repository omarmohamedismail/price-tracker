from playwright.sync_api import sync_playwright
import re
import requests
import os

TARGET_PRICE = 9999
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
PRODUCT_URL = "https://a.co/d/0gEox93f"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    response = requests.post(url, data={"chat_id": CHAT_ID, "text": text})
    print("رد تليجرام:", response.status_code, response.text)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(PRODUCT_URL)
    
    page.wait_for_timeout(3000)
    
    print("عنوان المنتج:", page.title())
    
    try:
        price_whole = re.sub(r"[^\d,]", "", page.locator(".a-price-whole").first.inner_text())
        price_fraction = re.sub(r"[^\d]", "", page.locator(".a-price-fraction").first.inner_text())
        
        current_price = float(price_whole.replace(",", "") + "." + price_fraction)
        
        print("السعر الحالي:", current_price)
        print("السعر المستهدف:", TARGET_PRICE)
        
        if current_price <= TARGET_PRICE:
            message = f"🎉 السعر نزل!\nالسعر الحالي: {current_price}\nالرابط: {PRODUCT_URL}"
            send_telegram_message(message)
        else:
            print("لسه السعر أعلى من اللي انت عايزه، هنراقب.")
            
    except Exception as e:
        print("معرفتش أقرا السعر، السبب:", e)
    
    browser.close()