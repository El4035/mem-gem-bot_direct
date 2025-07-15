from telegram import Bot

TOKEN = "8111573872:AAE_LGmsgtGmKmOxx2v03Tsd5bL28z9bL3Y"
CHAT_ID = 944484522
bot = Bot(token=TOKEN)

try:
    bot.send_message(chat_id=CHAT_ID, text="Проверка")
    print("✅ Сообщение отправлено")
except Exception as e:
    print(f"❌ Ошибка Telegram: {e}")
