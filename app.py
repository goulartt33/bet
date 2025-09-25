from flask import Flask
from telegram import Bot
from datetime import datetime
from football_real import get_football_bets
from basketball_real import get_basket_bets

app = Flask(__name__)

TELEGRAM_TOKEN = "7783572211:AAE99ISsfogVLk4r5fELoKzAVhwB_8okq-c"
TELEGRAM_CHAT_ID = "5538926378"
bot = Bot(token=TELEGRAM_TOKEN)

@app.route("/")
def home():
    return "✅ Bot de apostas online ativo!"

@app.route("/run-bets")
def run_bets():
    football_bets = get_football_bets()
    basket_bets = get_basket_bets()
    all_bets = football_bets + basket_bets

    for bet in all_bets:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"{datetime.now().strftime('%d/%m/%Y %H:%M')} | {bet}")
    
    return f"✅ {len(all_bets)} bilhetes enviados!"
