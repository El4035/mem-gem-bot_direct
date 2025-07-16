
import requests
import time
import threading
from flask import Flask

# Telegram config
TOKEN = '8111573872:AAE_LGmsgtGmKmOxx2v03Tsd5bL28z9bL3Y'
CHAT_ID = '944484522'

# Flask для Render
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

# Память отправленных
sent_ids = set()

# Функция для получения списка бирж по монете
def get_coin_exchanges(coin_id):
    url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/tickers'
    try:
        response = requests.get(url)
        data = response.json()
        exchanges = set()
        for item in data.get('tickers', []):
            exchange = item.get('market', {}).get('name', '').lower()
            if exchange:
                exchanges.add(exchange)
        return exchanges
    except:
        return set()

# Основной цикл
def scan_mem_gems():
    allowed_exchanges = {"kraken", "mexc", "bybit"}

    while True:
        try:
            print("🔁 Сканирую CoinGecko...")
            url = 'https://api.coingecko.com/api/v3/coins/markets'
            params = {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': 250,
                'page': 1,
                'sparkline': 'false'
            }
            response = requests.get(url, params=params)
            coins = response.json()

            for coin in coins:
                try:
                    coin_id = coin['id']
                    symbol = coin['symbol'].upper()
                    name = coin['name']
                    price = coin['current_price']
                    ath = coin['ath']
                    volume = coin['total_volume']
                    market_cap = coin['market_cap']

                    if ath == 0 or price == 0:
                        continue
                    drop = round(100 * (price - ath) / ath, 2)

                    # Фильтры
                    if coin_id in sent_ids:
                        continue
                    if price > 3:
                        continue
                    if volume < 1_000_000:
                        continue
                    if market_cap < 3_000_000:
                        continue
                    if drop > -75:
                        continue

                    tp1 = round(price * 1.272, 6)
                    tp2 = round(price * 1.618, 6)
                    tp3 = round(price * 2.0, 6)
                    tp4 = round(price * 2.618, 6)

                    if tp2 < price * 2:
                        continue

                    # Биржи
                    coin_exchanges = get_coin_exchanges(coin_id)
                    listed = sorted(set(e for e in coin_exchanges if e in allowed_exchanges))
                    if not listed:
                        continue

                    url_cg = f"https://www.coingecko.com/en/coins/{coin_id}"
                    rr = round(tp4 / price, 2)

                    message = f"""🚨 Мем-гем найден: {name} (${symbol})
📉 Цена: ${price}
📉 Падение от ATH: {drop}%
🎯 TP1: ${tp1}
🎯 TP2: ${tp2}
🎯 TP3: ${tp3}
🎯 TP4: ${tp4}
📊 Потенциал: x{rr}
📍 Торгуется на: {', '.join([ex.capitalize() for ex in listed])}
🔗 {url_cg}
"""
                    send_telegram_message(message)
                    sent_ids.add(coin_id)

                except:
                    continue

            time.sleep(180)

        except Exception as e:
            print("Ошибка:", e)
            time.sleep(180)

# Запуск
if __name__ == '__main__':
    send_telegram_message("🤖 Бот с CoinGecko и логикой запущен!")
    print("🚀 Бот запущен и работает...")
    threading.Thread(target=scan_mem_gems).start()
    app.run(host='0.0.0.0', port=10000)
