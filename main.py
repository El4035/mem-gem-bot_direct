
import requests
import time
import threading
from flask import Flask
import math

# Telegram config
TOKEN = '8111573872:AAE_LGmsgtGmKmOxx2v03Tsd5bL28z9bL3Y'
CHAT_ID = '944484522'

# Flask для поддержки Render 24/7
app = Flask(__name__)

@app.route('/')
def home():
    return "I'm alive!"

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {'chat_id': CHAT_ID, 'text': message}
    try:
        requests.post(url, data=payload)
    except:
        pass

# Память сигналов
sent_ids = set()

# Логика TP уровней
def calculate_targets(current_price):
    tp1 = round(current_price * 1.272, 6)
    tp2 = round(current_price * 1.618, 6)
    tp3 = round(current_price * 2.0, 6)
    tp4 = round(current_price * 2.618, 6)
    return tp1, tp2, tp3, tp4

# Основная логика
def scan_mem_gems():
    while True:
        try:
            print("🔁 Сканирую CoinGecko...")
            url = 'https://api.coingecko.com/api/v3/coins/markets'
            params = {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': 250,
                'page': 1,
                'sparkline': 'false',
                'price_change_percentage': '24h'
            }
            response = requests.get(url, params=params)
            coins = response.json()

            for coin in coins:
                try:
                    # Данные
                    coin_id = coin['id']
                    symbol = coin['symbol'].upper()
                    name = coin['name']
                    price = coin['current_price']
                    ath = coin['ath']
                    volume = coin['total_volume']
                    market_cap = coin['market_cap']

                    # Расчёты
                    if ath == 0 or price == 0:
                        continue
                    drop = round(100 * (price - ath) / ath, 2)
                    tp1, tp2, tp3, tp4 = calculate_targets(price)

                    # Фильтры
                    if coin_id in sent_ids:
                        continue
                    if price > 3:
                        continue
                    if volume < 1_000_000:
                        continue
                    if market_cap < 3_000_000:
                        continue
                    if drop > -75:  # теперь ослаблено до -75%
                        continue
                    if tp2 < price * 2:
                        continue  # потенциал должен быть минимум x2

                    # Отправка сигнала
                    url = f"https://www.coingecko.com/en/coins/{coin_id}"
                    message = f"🚨 Мем-гем найден: {name} (${symbol})\n"
                    message += f"📉 Цена: ${price}\n"
                    message += f"📉 Падение от ATH: {drop}%\n"
                    message += f"🎯 TP1: ${tp1}\n🎯 TP2: ${tp2}\n🎯 TP3: ${tp3}\n🎯 TP4: ${tp4}\n"

                    rr = round(tp4 / price, 2)
                    if rr >= 3:
                        message += f"🔥 Потенциал: x{rr} — High Potential\n"
                    else:
                        message += f"📊 Потенциал: x{rr}\n"

                    message += f"🔗 {url}"

                    send_telegram_message(message)
                    sent_ids.add(coin_id)

                except:
                    continue

            time.sleep(180)  # каждые 3 минуты

        except Exception as e:
            print("Ошибка:", e)
            time.sleep(180)

# Тестовый сигнал
def send_test_signal():
    message = (
        "🚨 TEST-сигнал: TESTCOIN\n"
        "📉 Цена: $0.01\n"
        "📉 Падение от ATH: -88%\n"
        "🎯 Цель (TP1): $0.0127\n"
        "🎯 Цель (TP2): $0.0161\n"
        "🎯 Цель (TP3): $0.02\n"
        "🎯 Цель (TP4): $0.0261\n"
        "📊 Потенциал: x2.6\n"
        "🔗 https://www.coingecko.com/en/coins/testcoin"
    )
    send_telegram_message(message)

# Запуск
if __name__ == '__main__':
    send_telegram_message("🤖 Бот с CoinGecko и логикой запущен!")
    print("🚀 Бот запущен — начинаю сканировать мем-гемов...")
    threading.Thread(target=scan_mem_gems).start()
    send_test_signal()
    app.run(host='0.0.0.0', port=10000)
