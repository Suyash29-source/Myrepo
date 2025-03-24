from flask import Flask, request
import telebot
import os

# ✅ Bot Token
API_TOKEN = "7806071446:AAFukCv3jKDCM8cQKnk0UevHzGjCl5QD13E"
bot = telebot.TeleBot(API_TOKEN)

# ✅ Flask App
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running with Webhook!"

# ✅ Telegram Webhook Endpoint
@app.route(f"/{API_TOKEN}", methods=["POST"])
def webhook():
    json_update = request.get_json()
    if json_update:
        bot.process_new_updates([telebot.types.Update.de_json(json_update)])
    return "!", 200

# ✅ Webhook Setup
def set_webhook():
    webhook_url = f"https://chatbook-58zq.onrender.com/{API_TOKEN}&max_connections=1000"
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)

if __name__ == "__main__":
    set_webhook()
    app.run(host="0.0.0.0", port=10000)
