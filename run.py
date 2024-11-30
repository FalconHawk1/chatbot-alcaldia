from threading import Thread
import subprocess

def run_flask():
    subprocess.run(["python", "app.py"])

def run_telegram():
    subprocess.run(["python", "telegram.py"])

if __name__ == "__main__":
    flask_thread = Thread(target=run_flask)
    telegram_thread = Thread(target=run_telegram)

    flask_thread.start()
    telegram_thread.start()

    flask_thread.join()
    telegram_thread.join()
