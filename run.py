from threading import Thread
import subprocess

def run_flask():
    subprocess.run(["python", "app.py"])

def run_telegram():
    subprocess.run(["python", "telegram.py"])

def run_report():
    subprocess.run(["python", "report.py"])

if __name__ == "__main__":
    flask_thread = Thread(target=run_flask)
    telegram_thread = Thread(target=run_telegram)
    report_thread = Thread(target=run_report)

    flask_thread.start()
    telegram_thread.start()
    report_thread.start()

    flask_thread.join()
    telegram_thread.join()
    report_thread.join()
