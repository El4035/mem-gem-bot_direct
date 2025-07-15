
from flask import Flask
from telegram import Bot
import requests

TOKEN = "8111573872:AAE_LGmsgtGmKmOxx2v03Tsd5bL28z9bL3Y"
CHAT_ID = 944484522

app = Flask(__name__)
bot = Bot(token=TOKEN)

def get_mem_gems():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 200,
        "page": 1,
        "price_change_percentage": "24h"
    }

    response = requests.get(url, params=params)
    coins = response.json()

    results = []
    for coin in coins:
        name = coin.get("name", "")
        symbol = coin.get("symbol", "").upper()
        price = coin.get("current_price", 0)
        ath = coin.get("ath", 1)
        market_cap = coin.get("market_cap", 0)
        volume = coin.get("total_volume", 0)

        if ath <= 0 or price <= 0:
            continue

        drop = (ath - price) / ath
        potential_x = ath / price if price != 0 else 0

        if drop >= 0.80 and potential_x >= 2 and market_cap > 5_000_000 and volume > 1_000_000 and price <= 3:
            if not any(x in symbol for x in ["USD", "USDT", "DAI", "TUSD", "BUSD"]):
                if symbol not in ["SCAM", "PIG", "TURD"]:
                    results.append(f"💎 {name} ({symbol})\nЦена: ${price:.4f}\nПотенциал: x{potential_x:.1f}")

    return results

@app.route("/")
def home():
    return "Mem-gem bot is running!"

if __name__ == "__main__":
    gems = get_mem_gems()
    if gems:
        for gem in gems:
            bot.send_message(chat_id=CHAT_ID, text=gem)
    else:
        bot.send_message(chat_id=CHAT_ID, text="⛔ Ничего не найдено по условиям (80–90% падение и x2 потенциал)")
    app.run(host="0.0.0.0", port=10000)
