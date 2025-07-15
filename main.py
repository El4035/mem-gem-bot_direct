import time
import requests
from flask import Flask
import threading

# === Telegram ===
TOKEN = "8111573872:AAE_LGmsgtGmKmOxx2v03Tsd5bL28z9bL3Y"
CHAT_ID = "944484522"

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        r = requests.post(url, data=payload)
        print("Telegram status:", r.status_code)
    except Exception as e:
        print("Ошибка при отправке сообщения:", e)

# === Flask для Render ===
app = Flask(__name__)

@app.route('/')
def home():
    return "I'm alive!"

@app.route('/send_test')
def send_test():
    send_message("✅ Test message sent!")
    return "Test message sent!"

def keep_alive():
    def run():
        app.run(host="0.0.0.0", port=10000)
    t = threading.Thread(target=run)
    t.start()

# === Основная логика ===
def get_mem_gems():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_asc",
        "per_page": 250,
        "page": 1,
        "sparkline": False
    }

    try:
        response = requests.get(url, params=params)
        coins = response.json()

        for coin in coins:
            try:
                name = coin["name"]
                symbol = coin["symbol"].upper()
                price = coin["current_price"]
                ath = coin["ath"]
                volume = coin["total_volume"]
                market_cap = coin["market_cap"]
                ath_change = coin["ath_change_percentage"]

                # Фильтры
                if (
                    not name or not symbol or price <= 0 or ath <= 0 or
                    market_cap is None or market_cap < 5_000_000 or
                    volume is None or volume < 1_000_000 or price > 3 or
                    any(stable in symbol for stable in ["USD", "USDT", "BUSD", "DAI", "TUSD"]) or
                    any(bad in symbol for bad in ["SCAM", "PIG", "TURD", "RUG", "ASS"])
                ):
                    continue

                drop_pct = round((1 - price / ath) * 100, 2)
                if not (80 <= drop_pct <= 90):
                    continue

                # Фибоначчи цели
                tp1 = round(price * 1.272, 6)
                tp2 = round(price * 1.618, 6)
                tp3 = round(price * 2.0, 6)
                tp4 = round(price * 2.618, 6)

                msg = f"""🚀 Найден мем-гем!

🔸 Название: {name} ({symbol})
💲 Цена: ${price}
📉 Падение от ATH: -{drop_pct:.1f}%
📊 Объём: ${volume:,.0f}
🎯 Цели (Fibonacci):
• TP1 (1.272): ${tp1}
• TP2 (1.618): ${tp2}
• TP3 (2.0):   ${tp3}
• TP4 (2.618): ${tp4}

🔗 https://www.coingecko.com/en/coins/{coin['id']}
#memgem #crypto #potential
"""
                send_message(msg)

            except Exception as e:
                print("Ошибка при проверке монеты:", e)

    except Exception as e:
        print("Ошибка при получении данных:", e)

def main_loop():
    while True:
        try:
            print("🔄 Сканирование мем-гемов...")
            get_mem_gems()
        except Exception as e:
            print("Ошибка в основном цикле:", e)
        time.sleep(180)

# === Запуск ===
keep_alive()
send_message("🤖 Бот с CoinGecko и логикой запущен!")
main_loop()
