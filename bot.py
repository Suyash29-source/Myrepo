from flask import Flask
import threading
import os
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# ✅ Restart bot every 20 mins to prevent timeout
def restart_bot():
    while True:
        os.system("python chatbook.py")  # Run the bot
        time.sleep(150)  # Restart every 20 minutes

# ✅ Run bot in a separate thread
threading.Thread(target=restart_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
