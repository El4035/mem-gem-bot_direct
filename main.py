import time
import requests
import csv
from flask import Flask
from telegram import Bot

TOKEN = "8111573872:AAE_LGmsgtGmKmOxx2v03Tsd5bL28z9bL3Y"
CHAT_ID = 944484522

bot = Bot(token=TOKEN)
app = Flask(__name__)

# Чёрный список тикеров
blacklist = {"SCAM", "PIG", "TURD", "ASS", "RUG", "HITLER", "FLOKICEO", "KYS", "TRUMPLOVER"}

def get_top_coins():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 200,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "24h"
    }
    response = requests.get(url, params=params)
    return response.json()

def passes_filters(coin):
    symbol = coin['symbol'].upper()
    name = coin['name'].upper()
    price = coin['current_price']
    vol = coin['total_volume']
    cap = coin['market_cap']
    exchanges = [e['name'] for e in coin.get("tickers", [])]

    if any(stable in symbol for stable in ["USD", "USDT", "BUSD", "DAI", "TUSD"]):
        return False
    if any(bad in symbol for bad in blacklist):
        return False
    if price > 3 or price <= 0:
        return False
    if vol < 1_000_000:
        return False
    if cap is None or cap < 5_000_000:
        return False
    return True

def check_coins():
    try:
        coins = get_top_coins()
        for coin in coins:
            if not passes_filters(coin):
                continue
            ath = coin.get("ath", 0)
            current = coin.get("current_price", 0)
            if ath <= 0 or current <= 0:
                continue
            drop_pct = (1 - current / ath) * 100
            if drop_pct < 80:
                continue

            symbol = coin['symbol'].upper()
            name = coin['name']
            price = coin['current_price']
            url = f"https://www.coingecko.com/en/coins/{coin['id']}"

            message = f"🚨 *HIGH POTENTIAL MEM COIN*\n\n🔸 *{name.upper()}*  (${symbol})\n💰 Цена: ${price}\n📉 Упало от ATH: {drop_pct:.1f}%\n🔗 [CoinGecko]({url})"
            bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown', disable_web_page_preview=False)

            # лог
            with open("signals_log.csv", "a") as f:
                writer = csv.writer(f)
                writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), name, symbol, price, f"{drop_pct:.1f}%"])
    except Exception as e:
        print(f"Error: {e}")

@app.route('/')
def home():
    return "Mem Gem Bot is running!"

if __name__ == "__main__":
    print("Mem-Gem Bot запущен ✅")
    bot.send_message(chat_id=CHAT_ID, text="✅ Mem-Gem Бот запущен на Render.")
    while True:
        check_coins()
        time.sleep(180)  # проверка каждые 3 минуты
