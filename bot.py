from flask import Flask, request
import telebot
import bot  # 🔹 bot.py ko import kar diya
import os

TOKEN = "7806071446:AAFukCv3jKDCM8cQKnk0UevHzGjCl5QD13E"
bot_instance = telebot.TeleBot(TOKEN)  # 🔹 bot.py ka bot object use karne ke liye ek instance

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot_instance.process_new_updates([update])  # 🔹 bot.py ka bot instance use kar ke update process karna
    return 'OK', 200

if __name__ == "__main__":
    bot_instance.remove_webhook()
    bot_instance.set_webhook(url="https://chatbook-igjr.onrender.com" + TOKEN)
    app.run(host="0.0.0.0", port=10000)
