# 🔍 Telegram Product Search Bot

An automated bot that lets you search for products via Telegram and get instant results — built with Python, Playwright, and the Telegram Bot API.

## The Problem It Solves

Manually checking multiple products or prices takes time. This bot automates the search process: send a product name to Telegram, and the bot browses the target site and returns matching results (name + price) in seconds.

## How It Works

1. **Playwright** launches a headless browser and navigates the target site.
2. The bot searches across all listing pages for matches to your query.
3. Results are sent back to you instantly via **Telegram**.
4. Hosted and run through **GitHub Actions** — no local machine required.

## Tech Stack

- Python
- Playwright (browser automation)
- python-telegram-bot (Telegram integration)
- GitHub Actions (cloud execution)

## How to Run It Yourself

1. Clone this repo
2. Install dependencies:
pip install -r requirements.txt
playwright install
3. Set environment variables `TELEGRAM_TOKEN` and `CHAT_ID`
4. Run:
python price_check.py
5. Message your bot on Telegram with any search term

## Demo

_[Add a short screen recording or GIF here showing the bot responding to a message]_

---

Built as part of a hands-on automation learning project.