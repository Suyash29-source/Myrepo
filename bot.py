import telebot
import random
import threading
import time
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = "7806071446:AAFukCv3jKDCM8cQKnk0UevHzGjCl5QD13E"
bot = telebot.TeleBot(API_TOKEN)

queue = []  # Users waiting for chat
chats = {}  # Active chat pairs
reported_users = set()  # Users who are reported
spy_chats = []  # Spy chat group


# ✅ Fake Online Users Count
def get_fake_online_count():
    return random.randint(2500, 5000)  # Random fake count


# ✅ Start Command (Improved with Buttons)
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("🔍 Find Chat"))
    keyboard.add(KeyboardButton("👥 Join Spy Chat"), KeyboardButton("❌ End Chat"))

    bot.send_message(
        user_id,
        f"🔥 Welcome to *ChatBookBot!* 🎉\n\n"
        f"🔹 *{get_fake_online_count()} users* are chatting right now!\n"
        f"💬 Meet new people & chat anonymously.\n\n"
        f"✅ *Commands:*\n"
        f"🔹 /find - Start random chat\n"
        f"🔹 /spy - Join anonymous group chat\n"
        f"🔹 /next - Find a new partner\n"
        f"🔹 /report - Report bad user\n"
        f"🔹 /end - Disconnect chat\n\n"
        f"⚠️ *Rules:*\n"
        f"❌ No spamming\n"
        f"❌ No abuse\n"
        f"❌ Be respectful!\n\n"
        f"💡 Stay safe & enjoy chatting!",
        parse_mode="Markdown",
        reply_markup=keyboard
    )


# ✅ Find Partner
@bot.message_handler(commands=['find'])
@bot.message_handler(func=lambda message: message.text == "🔍 Find Chat")
def find_chat(message):
    user_id = message.chat.id

    if user_id in chats or user_id in queue:
        bot.send_message(user_id, "⚠️ You are already in a chat!")
        return

    queue.append(user_id)
    bot.send_message(user_id, f"🔍 Searching for a partner... ({get_fake_online_count()} online)")

    if len(queue) >= 2:
        user1 = queue.pop(0)
        user2 = queue.pop(0)

        if user1 != user2:
            chats[user1] = user2
            chats[user2] = user1

            bot.send_message(user1, "✅ Partner found! Start chatting.")
            bot.send_message(user2, "✅ Partner found! Start chatting.")

            # Start auto-disconnect timer
            threading.Thread(target=auto_disconnect_timer, args=(user1, user2)).start()


# ✅ Auto-Disconnect Timer (3 mins inactivity)
def auto_disconnect_timer(user1, user2):
    time.sleep(180)  # 3 minutes
    if user1 in chats and chats[user1] == user2:
        bot.send_message(user1, "⏳ 3 minutes up! Chat ended. Type /find to search again.")
        bot.send_message(user2, "⏳ 3 minutes up! Chat ended. Type /find to search again.")
        disconnect_users(user1, user2)


# ✅ Disconnect Users
@bot.message_handler(commands=['end'])
@bot.message_handler(func=lambda message: message.text == "❌ End Chat")
def end_chat(message):
    user_id = message.chat.id
    if user_id in chats:
        partner_id = chats[user_id]
        bot.send_message(partner_id, "❌ Chat ended. Type /find to search again.")
        bot.send_message(user_id, "❌ Chat ended. Type /find to search again.")
        disconnect_users(user_id, partner_id)
    else:
        bot.send_message(user_id, "⚠️ You're not in a chat!")


# ✅ Handle Messages (Forwarding with Typing Indicator)
@bot.message_handler(func=lambda message: message.chat.id in chats)
def forward_message(message):
    sender_id = message.chat.id
    receiver_id = chats.get(sender_id)

    if receiver_id:
        bot.send_chat_action(receiver_id, 'typing')  # ✅ Typing Indicator
        bot.send_message(receiver_id, f"👤: {message.text}")


# ✅ Handle Images & Media
@bot.message_handler(content_types=['photo', 'audio', 'video', 'voice'])
def handle_media(message):
    sender_id = message.chat.id
    receiver_id = chats.get(sender_id)

    if receiver_id:
        bot.forward_message(receiver_id, sender_id, message.message_id)


# ✅ Reporting System
@bot.message_handler(commands=['report'])
def report_user(message):
    user_id = message.chat.id
    if user_id in chats:
        reported_users.add(chats[user_id])
        bot.send_message(user_id, "⚠️ User reported. Searching for a new chat...")
        disconnect_users(user_id, chats[user_id])


# ✅ Spy Mode (Anonymous Group Chat)
@bot.message_handler(commands=['spy'])
@bot.message_handler(func=lambda message: message.text == "👥 Join Spy Chat")
def join_spy_chat(message):
    user_id = message.chat.id

    if user_id not in spy_chats:
        spy_chats.append(user_id)
        bot.send_message(user_id, "👀 Joined anonymous group chat! Send messages now.")

        # Notify others in the chat
        for user in spy_chats:
            if user != user_id:
                bot.send_message(user, "👤 New user joined anonymous chat!")


# ✅ Handle Spy Chat Messages
@bot.message_handler(func=lambda message: message.chat.id in spy_chats)
def handle_spy_messages(message):
    user_id = message.chat.id
    for user in spy_chats:
        if user != user_id:
            bot.send_message(user, f"🕵️ {message.text}")


# ✅ Instant Reconnect Feature
@bot.message_handler(commands=['next'])
def instant_reconnect(message):
    user_id = message.chat.id
    if user_id in chats:
        disconnect_users(user_id, chats[user_id])
    find_chat(message)


# ✅ Start the Bot
bot.polling()
