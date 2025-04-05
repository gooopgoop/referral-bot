import logging
from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# Telegram bot config
BOT_TOKEN = "7922079451:AAGRBDCzesT2T2YmSUFHzPk4QlW-6fKIYFs"
CHAT_ID = "-1002636580415"

# Логгер
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Хранилище переходов (можно заменить на базу данных)
clicks = {}

@app.route("/")
def index():
    return "Referral bot is running."

@app.route("/go")
def go():
    sid = request.args.get("sid")
    if not sid:
        return "Missing SID", 400

    # Сохраняем информацию о переходе
    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent")

    clicks[sid] = clicks.get(sid, 0) + 1

    msg = f"\ud83d\udd17 Переход по ссылке\nSID: {sid}\nIP: {ip}\nUA: {user_agent}"
    send_to_telegram(msg)

    # Перенаправление на реальную ссылку
    target_url = f"https://datingforyou7.cfd/slinckpartnersnew/?flow=26993&utm_source={sid}&utm_content=click"
    return redirect(target_url)

@app.route("/postback")
def postback():
    sid = request.args.get("subid")
    status = request.args.get("status", "unknown")

    msg = f"\u2705 Конверсия!\nSID: {sid}\nСтатус: {status}"
    send_to_telegram(msg)
    return "OK"

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        logger.error(f"Telegram error: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
