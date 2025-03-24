from flask import Flask, request
import telebot
import os
import chatbook  # ✅ Bot ka code import kiya

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running with Webhook!"

@app.route(f"/{chatbook.API_TOKEN}", methods=["POST"])
def webhook():
    json_update = request.get_json()
    if json_update:
        chatbook.bot.process_new_updates([telebot.types.Update.de_json(json_update)])
    return "OK", 200

if __name__ == "__main__":
    chatbook.bot.remove_webhook()  # ✅ Purana webhook hatao
    chatbook.bot.set_webhook(url=f"https://chatbook-58zq.onrender.com/{chatbook.API_TOKEN}")  # ✅ Naya webhook set karo
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))