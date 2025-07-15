from telegram import Bot

TOKEN = "8111573872:AAE_LGmsgtGmKmOxx2v03Tsd5bL28z9bL3Y"
CHAT_ID = 944484522
bot = Bot(token=TOKEN)

print("🚀 Старт: бот запустился")

try:
    bot.send_message(chat_id=CHAT_ID, text="✅ Бот запущен и работает!")
    print("✅ Сообщение отправлено успешно")
except Exception as e:
    print(f"❌ Ошибка Telegram: {e}")
