import telebot
import random

API_TOKEN = "7806071446:AAFukCv3jKDCM8cQKnk0UevHzGjCl5QD13E"
bot = telebot.TeleBot(API_TOKEN)

queue = []  # Users waiting for chat
chats = {}  # Active chat pairs

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome to ChatBook! Type /find to start chatting with a random person.")

@bot.message_handler(commands=['find'])
def find_chat(message):
    user_id = message.chat.id
    if user_id in chats:
        bot.send_message(user_id, "You're already in a chat! Type /end to leave.")
        return

    if len(queue) > 0:
        partner_id = queue.pop(0)
        chats[user_id] = partner_id
        chats[partner_id] = user_id
        bot.send_message(user_id, "✅ Connected! Start chatting now. Type /end to disconnect.")
        bot.send_message(partner_id, "✅ Connected! Start chatting now. Type /end to disconnect.")
    else:
        queue.append(user_id)
        bot.send_message(user_id, "🔄 Searching for a partner... Please wait!")

@bot.message_handler(commands=['end'])
def end_chat(message):
    user_id = message.chat.id
    if user_id in chats:
        partner_id = chats[user_id]
        del chats[user_id]
        del chats[partner_id]
        bot.send_message(user_id, "❌ Chat ended. Type /find to search again.")
        bot.send_message(partner_id, "❌ Chat ended. Type /find to search again.")
    else:
        bot.send_message(user_id, "❌ You're not in a chat!")

@bot.message_handler(func=lambda message: True)
def forward_message(message):
    user_id = message.chat.id
    if user_id in chats:
        partner_id = chats[user_id]
        bot.send_message(partner_id, message.text)

bot.polling()
