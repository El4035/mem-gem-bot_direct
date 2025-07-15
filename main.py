import time
import threading
from flask import Flask
from telegram import Bot

# === Конфигурация ===
BOT_TOKEN = "8111573872:AAE_LGmsgtGmKmOxx2v03Tsd5bL28z9bL3Y"
CHAT_ID = "944484522"
UPDATE_INTERVAL = 180  # каждые 3 минуты

bot = Bot(token=BOT_TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return 'Mem-Gem Bot is running!'

def send_message(text):
    try:
        bot.send_message(chat_id=CHAT_ID, text=text)
    except Exception as e:
        print(f"[Telegram Error] {e}")

def check_signals():
    while True:
        try:
            # Здесь будет логика мем-гем фильтра. Пока тест:
            send_message("✅ Мем-гем бот работает! (тестовое сообщение)")
        except Exception as e:
            print(f"[Signal Check Error] {e}")
        time.sleep(UPDATE_INTERVAL)

if __name__ == '__main__':
    threading.Thread(target=check_signals).start()
    app.run(host='0.0.0.0', port=10000)