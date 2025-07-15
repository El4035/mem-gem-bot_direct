import requests
from flask import Flask
from telegram import Bot

TOKEN = "8111573872:AAE_LGmsgtGmKmOxx2v03Tsd5bL28z9bL3Y"
CHAT_ID = 944484522
bot = Bot(token=TOKEN)

app = Flask(__name__)

# Получение списка мем-гемов
def get_mem_gems():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 200,
        "page": 1,
        "sparkline": "false"
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        gems = []
        for coin in data:
            name = coin["name"]
            symbol = coin["symbol"]
            price = coin["current_price"]
            ath = coin["ath"]
            volume = coin["total_volume"]
            market_cap = coin["market_cap"]
            if (
                ath > 0 and
                price > 0 and
                market_cap and market_cap > 5_000_000 and
                volume and volume > 1_000_000 and
                "usd" not in symbol.lower() and
                "usdt" not in symbol.lower() and
                "busd" not in symbol.lower() and
                "dai" not in symbol.lower() and
                "tusd" not in symbol.lower() and
                "scam" not in symbol.lower() and
                "pig" not in symbol.lower() and
                "turd" not in symbol.lower()
            ):
                drop_pct = 100 * (1 - price / ath)
                if 80 <= drop_pct <= 90 and price * 2 <= ath:
                    gems.append(f"{name.upper()} ({symbol.upper()}): ${price} | Drop: {drop_pct:.1f}% | ATH: ${ath}")
        return gems
    except Exception as e:
        print("Error getting mem gems:", e)
        return []

@app.route("/")
def home():
    return "Bot is running!"

@app.route("/send_test")
def send_test():
    bot.send_message(chat_id=CHAT_ID, text="✅ Test message from mem-gem bot!")
    return "Test message sent!"

if __name__ == "__main__":
    gems = get_mem_gems()
    if gems:
        for gem in gems:
            bot.send_message(chat_id=CHAT_ID, text=f"💎 MEM-GEM:\n{gem}")
    else:
        bot.send_message(chat_id=CHAT_ID, text="❗️Мем-гемов не найдено")
    app.run(host="0.0.0.0", port=10000)
