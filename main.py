import time
import requests
from flask import Flask
from telegram import Bot

# === Конфигурация ===
TOKEN = "8111573872:AAE_LGmsgtGmKmOxx2v03Tsd5bL28z9bL3Y"
CHAT_ID = 944484522
bot = Bot(token=TOKEN)

# === Flask-сервер для Render и UptimeRobot ===
app = Flask(__name__)

@app.route('/')
def home():
    return "I'm alive!"

@app.route('/send_test')
def send_test():
    bot.send_message(chat_id=CHAT_ID, text="✅ Тестовое сообщение отправлено!")
    return "Test message sent!"

# === Логика MEM-GEM анализа ===
def get_mem_gems():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_asc",
            "per_page": 250,
            "page": 1,
            "price_change_percentage": "24h"
        }
        response = requests.get(url, params=params)
        data = response.json()

        for coin in data:
            name = coin['name']
            symbol = coin['symbol']
            price = coin['current_price']
            ath = coin['ath']
            volume = coin['total_volume']

            if not ath or ath == 0:
                continue

            drop_percent = ((price - ath) / ath) * 100

            # Условия: падение на 80-90% и объём > $1M
            if -95 <= drop_percent <= -80 and volume >= 1_000_000:
                # Фибоначчи цели
                tp1 = round(price * 1.272, 6)
                tp2 = round(price * 1.618, 6)
                tp3 = round(price * 2.0, 6)
                tp4 = round(price * 2.618, 6)

                high_potential = "🔥 High Potential!" if tp4 >= price * 3 else ""

                message = (
                    f"🚀 <b>{name.upper()}</b> (${symbol.upper()})\n"
                    f"💰 Цена: <b>${price}</b>\n"
                    f"📉 Падение от ATH: <b>{round(drop_percent, 2)}%</b>\n"
                    f"📈 Цели роста:\n"
                    f"— TP1: ${tp1}\n"
                    f"— TP2: ${tp2}\n"
                    f"— TP3: ${tp3}\n"
                    f"— TP4: ${tp4}\n"
                    f"{high_potential}\n"
                    f"\n🔗 <a href='https://www.coingecko.com/en/coins/{coin['id']}'>График CoinGecko</a>"
                )

                bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="HTML")

    except Exception as e:
        print(f"Ошибка при получении мем-гемов: {e}")

# === Основной цикл ===
def main_loop():
    while True:
        try:
            print("🔍 Поиск MEM-GEM монет...")
            get_mem_gems()
        except Exception as e:
            print(f"Ошибка в основном цикле: {e}")
        time.sleep(180)  # обновление каждые 3 минуты

# === Запуск ===
def keep_alive():
    import threading
    def run():
        app.run(host="0.0.0.0", port=10000)
    t = threading.Thread(target=run)
    t.start()

keep_alive()
main_loop()
