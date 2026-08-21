from playwright.async_api import async_playwright
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import os

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
MAX_RESULTS = 10

async def search_books(query):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        results = []
        page_number = 1
        
        while True:
            url = f"https://books.toscrape.com/catalogue/page-{page_number}.html"
            response = await page.goto(url)
            
            if response.status != 200:
                break  # وصلنا لآخر صفحة
            
            await page.wait_for_timeout(500)
            
            books = page.locator("article.product_pod")
            count = await books.count()
            print(f"صفحة {page_number}: عدد الكتب = {count}")
            
            for i in range(count):
                book = books.nth(i)
                name = await book.locator("h3 a").get_attribute("title")
                if query.lower() in name.lower():
                    price = await book.locator(".price_color").inner_text()
                    results.append(f"{name}\nالسعر: {price}")
                    print(f"لقينا تطابق: {name}")
            
            if len(results) >= MAX_RESULTS:
                break
            
            page_number += 1
            if page_number > 50:  # حد أمان يمنع لوب لا نهائي
                break
        
        await browser.close()
        return results[:MAX_RESULTS]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text(f"🔍 بدور على: {query} ...")
    
    results = await search_books(query)
    
    if results:
        message = f"لقيت {len(results)} نتيجة:\n\n" + "\n\n".join(results)
    else:
        message = "معلش، مفيش نتائج مطابقة."
    
    await update.message.reply_text(message)

app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("البوت شغال، استنى الرسايل...")
app.run_polling()