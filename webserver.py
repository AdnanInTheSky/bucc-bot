"""
Simple Flask web server for health checks and keeping the bot alive on free hosting platforms.
"""
from flask import Flask
from threading import Thread
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "BUCC Discord Bot is running!", 200

@app.route('/health')
def health():
    return {"status": "healthy", "bot": "BUCC Discord Bot"}, 200

def run():
    """Run Flask server on port specified by environment or default to 8080"""
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    """Start Flask server in a separate thread"""
    t = Thread(target=run)
    t.daemon = True
    t.start()
