from flask import Flask
from threading import Thread
import logging

logger = logging.getLogger(__name__)

app = Flask("")


@app.route("/")
def home():
    """Defines the home route for the Flask app."""
    return "Bot is alive!"


def run():
    """
    Runs the Flask application.

    This function starts the web server that keeps the bot alive.
    """
    try:
        app.run(host="0.0.0.0", port=8080)
    except Exception as e:
        logger.error(f"Error running Flask app: {e}")


def keep_alive():
    """
    Starts a new thread to run the Flask application.

    This function is called to keep the bot's process alive, especially when deployed
    on platforms that require a web server to be running.
    The thread is set as a daemon thread, so it will terminate when the main program exits.
    """
    t = Thread(target=run, daemon=True)
    t.start()
    logger.info("Keep-alive server started.")
