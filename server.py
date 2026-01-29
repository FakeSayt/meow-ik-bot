from flask import Flask
from threading import Thread
from config import PORT

app = Flask(__name__)

@app.route("/")
def home():
    return "Discord bot is running!"

def run_web():
    app.run(host="0.0.0.0", port=PORT)

def start_server():
    Thread(target=run_web).start()
