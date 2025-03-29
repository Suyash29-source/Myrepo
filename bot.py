from flask import Flask, request
import telebot

TOKEN = "7806071446:AAFukCv3jKDCM8cQKnk0UevHzGjCl5QD13E"
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    try:
        json_str = request.get_data().decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)
        print("🚀 Request Received:", json_str)  # Debugging ke liye print karo
        bot.process_new_updates([update])  # ✅ Yeh bot ko update bhejega
    except Exception as e:
        print("❌ Error:", str(e))  # Agar koi error aaye toh print kare
    return 'OK', 200

# ✅ Bot Commands Handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "✅ Bot is working! Send any message.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, f"📩 You sent: {message.text}")


@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    try:
        json_str = request.get_data().decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)
        print("🚀 Request Received:", json_str)  
        print("✅ Processing Update...")  # Debugging ke liye

        bot.process_new_updates([update])  # ✅ Yeh update process karega
        print("✅ Update Processed!")  # Debugging ke liye

    except Exception as e:
        print("❌ Error:", str(e))  # Agar koi error aaye toh print kare

    return 'OK', 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://chatbook-igjr.onrender.com/" + TOKEN)
    app.run(host="0.0.0.0", port=10000)
