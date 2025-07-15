from flask import Flask
from telegram import Bot

TOKEN = "8111573872:AAE_LGmsgtGmKmOxx2v03Tsd5bL28z9bL3Y"
CHAT_ID = 944484522

app = Flask(__name__)
bot = Bot(token=TOKEN)

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == "__main__":
    bot.send_message(chat_id=CHAT_ID, text="✅ Bot запущен!")
    app.run(host="0.0.0.0", port=10000)
