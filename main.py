import os
import telegram
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHANNEL_ID")
bot = telegram.Bot(token=TOKEN)

@app.route("/signal", methods=["POST"])
def signal():
    data = request.json
    if not data:
        return "No data", 400

    # محتوى التنبيه حسب نوع الصفقة
    signal_type = data.get("type")
    pair = data.get("pair", "زوج غير محدد")
    timeframe = data.get("timeframe", "فريم غير معروف")
    duration = data.get("duration", "مدة غير معروفة")

    if signal_type == "buy":
        msg = f"🚀 صفقة شراء على {pair} - فريم {timeframe} - مدة الصفقة: {duration} دقيقة"
    elif signal_type == "sell":
        msg = f"🔻 صفقة بيع على {pair} - فريم {timeframe} - مدة الصفقة: {duration} دقيقة"
    elif signal_type == "mt5":
        entry = data.get("entry")
        sl = data.get("sl")
        tp1 = data.get("tp1")
        tp2 = data.get("tp2")
        msg = (
            f"🧠 صفقة MT5\n"
            f"الزوج: {pair}\n"
            f"نوع الصفقة: {'شراء' if data.get('direction') == 'buy' else 'بيع'}\n"
            f"سعر الدخول: {entry}\n"
            f"وقف الخسارة: {sl}\n"
            f"الأهداف: TP1 = {tp1}, TP2 = {tp2}"
        )
    else:
        msg = "📌 إشارة غير معروفة تم استلامها"

    bot.send_message(chat_id=CHAT_ID, text=msg)
    return "Signal sent!", 200

@app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
