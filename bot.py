from flask import Flask, request
import telebot
import threading
import os

API_TOKEN = "7806071446:AAFukCv3jKDCM8cQKnk0UevHzGjCl5QD13E"
bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running with Webhook!"

@app.route(f"/{API_TOKEN}", methods=["POST"])
def webhook():
    json_update = request.get_json()
    if json_update:
        bot.process_new_updates([telebot.types.Update.de_json(json_update)])
    return "!", 200

def run_bot():
    bot.remove_webhook()
    bot.set_webhook(url=f"https://chatbook-58zq.onrender.com/{API_TOKEN}")
    bot.infinity_polling()

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
