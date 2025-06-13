import os
from telegram import Bot
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHANNEL_ID")
bot = Bot(token=TOKEN)

@app.route("/signal", methods=["POST"])
def signal():
    data = request.json
    if not data:
        return "No data", 400

    # محتوى التنبيه حسب نوع الصفقة
    signal_type = data.get("type")
    pair = data.get("pair")
    timeframe = data.get("timeframe")
    duration = data.get("duration")

    message = ""
    if signal_type == "buy":
        message = f"🚀 شراء على {pair} - فريم {timeframe} - مدة الصفقة: {duration} دقائق"
    elif signal_type == "sell":
        message = f"🔻 بيع على {pair} - فريم {timeframe} - مدة الصفقة: {duration} دقائق"
    else:
        message = "إشارة غير معروفة"

    bot.send_message(chat_id=CHAT_ID, text=message)
    return "تم إرسال الإشارة", 200

if __name__ == "__main__":
    app.run(debug=True)
