from flask import Flask
import threading
import os

# ✅ Dummy Flask Server (Render ke liye)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# ✅ Background me chatbook.py ko run karne ka function
def run_bot():
    os.system("python chatbook.py")

# ✅ Bot ko alag thread me start karna (taaki Flask block na kare)
threading.Thread(target=run_bot).start()

# ✅ Flask server start karein (Render ke liye)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
