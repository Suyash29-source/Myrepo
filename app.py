from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, emit
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)

# Load or create users file
users_file = 'users.txt'
if not os.path.exists(users_file):
    with open(users_file, 'w') as f:
        f.write('')

# Load or create private chat messages file
if not os.path.exists('private_chats.json'):
    with open('private_chats.json', 'w') as f:
        json.dump({}, f)

# Load or create private chat folder
if not os.path.exists('private_chat'):
    os.makedirs('private_chat')

# Load users from the file
def load_users():
    with open(users_file, 'r') as f:
        return f.read().splitlines()

# Save users to the file
def save_users(username, password):
    with open(users_file, 'a') as f:
        f.write(f'{username},{password}\n')

# Authenticate user
def authenticate(username, password):
    users = load_users()
    return f"{username},{password}" in users

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        save_users(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# SocketIO for private chat
@socketio.on('private_message')
def handle_private_message(data):
    username = data['username']
    message = data['message']
    # Save message to the corresponding private chat file
    filename = f'private_chat/{username}chats.json'
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump([], f)
    
    with open(filename, 'r') as f:
        chats = json.load(f)
    
    chats.append({'username': session['username'], 'message': message})
    
    with open(filename, 'w') as f:
        json.dump(chats, f)

    emit('private_message', {'username': session['username'], 'message': message}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)