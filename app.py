from flask import Flask
from telegram import Bot
import os
from datetime import datetime
import random
import threading
import time

# =========================
# Configuração do Telegram
# =========================
TELEGRAM_TOKEN = "7783572211:AAE99ISsfogVLk4r5fELoKzAVhwB_8okq-c"
TELEGRAM_CHAT_ID = "5538926378"
bot = Bot(token=TELEGRAM_TOKEN)

# =========================
# Flask App
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "🤖 Bot de Apostas Online Ativo!"

# =========================
# Funções de geração de bilhetes
# =========================
def generate_football_bets():
    teams = ["Flamengo", "Palmeiras", "Corinthians", "Santos"]
    bets = []
    for _ in range(3):
        home = random.choice(teams)
        away = random.choice([t for t in teams if t != home])
        line = random.choice(["Over 1.5", "Under 2.5", "Ambas marcam"])
        odd = round(random.uniform(1.50, 2.50), 2)
        bets.append(f"⚽ {home} x {away} | {line} @ {odd}")
    return bets

def generate_basketball_bets():
    teams = ["Lakers", "Bulls", "Heat", "Celtics"]
    bets = []
    for _ in range(2):
        home = random.choice(teams)
        away = random.choice([t for t in teams if t != home])
        line = random.choice(["Over 210.5", "Under 215.5"])
        odd = round(random.uniform(1.70, 2.10), 2)
        bets.append(f"🏀 {home} x {away} | {line} @ {odd}")
    return bets

# =========================
# Envio de bilhetes
# =========================
def send_bets():
    football_bets = generate_football_bets()
    basketball_bets = generate_basketball_bets()
    all_bets = football_bets + basketball_bets
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    for bet in all_bets:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"{timestamp} | {bet}")

# =========================
# Scheduler interno
# =========================
def scheduler(interval_minutes=30):
    while True:
        try:
            send_bets()
        except Exception as e:
            print(f"Erro ao enviar bilhetes: {e}")
        time.sleep(interval_minutes * 60)

# Start scheduler em thread separada
threading.Thread(target=scheduler, daemon=True).start()

# =========================
# Rota manual (opcional)
# =========================
@app.route("/run-bets")
def run_bets():
    send_bets()
    return "✅ Bilhetes enviados manualmente!"

# =========================
# Main
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
