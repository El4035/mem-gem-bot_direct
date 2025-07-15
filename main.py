import requests
import time
from flask import Flask
import threading
import datetime
import telegram

# === Настройки Telegram ===
TOKEN = "8111573872:AAE_LGmsgtGmKmOxx2v03Tsd5bL28z9bL3Y"
CHAT_ID = "944484522"
bot = telegram.Bot(token=TOKEN)

# === Flask сервер для Render (чтобы не засыпал) ===
app = Flask(__name__)

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    thread = threading.Thread(target=run)
    thread.start()

# === Проверка монет на мем-гем ===
def check_mem_gems():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_asc",
        "per_page": 250,
        "page": 1,
        "sparkline": False
    }

    response = requests.get(url, params=params)
    coins = response.json()

    for coin in coins:
        try:
            name = coin["name"]
            symbol = coin["symbol"].upper()
            price = coin["current_price"]
            ath = coin["ath"]
            ath_change = coin["ath_change_percentage"]
            volume = coin["total_volume"]
            market_cap = coin["market_cap"]

            # === Фильтры ===
            if ath_change < -80 and price <= 1 and market_cap and market_cap >= 5000000 and volume >= 1000000:
                # Расчёт целей (TP1–TP4) от текущей цены
                tp1 = round(price * 1.272, 4)
                tp2 = round(price * 1.618, 4)
                tp3 = round(price * 2.0, 4)
                tp4 = round(price * 2.618, 4)

                msg = f"""
🚨 <b>High Potential MEM-GEM</b> 🚨
<b>{name} ({symbol})</b>

📉 Price: ${price}
🔻 Down from ATH: {round(ath_change, 2)}%
💰 Volume: ${volume:,}
🏦 Market Cap: ${market_cap:,}

🎯 Targets:
TP1: ${tp1}
TP2: ${tp2}
TP3: ${tp3}
TP4: ${tp4}

#memgem #crypto #potential
"""
                bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode=telegram.ParseMode.HTML)

        except Exception as e:
            print("Ошибка при проверке монеты:", e)

# === Основной цикл автообновления ===
def main_loop():
    while True:
        try:
            print("🔄 Поиск мем-гемов:", datetime.datetime.now())
            check_mem_gems()
        except Exception as e:
            print("Ошибка в основном цикле:", e)
        time.sleep(180)  # обновление каждые 3 минуты

# === Запуск ===
keep_alive()
main_loop()
@app.route("/send_test")
def send_test():
    bot.send_message(chat_id=CHAT_ID, text="✅ Test message from mem-gem bot")
    return "Test message sent!"
