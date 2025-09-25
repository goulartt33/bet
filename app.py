from flask import Flask
from telegram import Bot
import os
from datetime import datetime
import random

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
    # Aqui você pode colocar lógica real baseada em estatísticas
    teams = ["Flamengo", "Palmeiras", "Corinthians", "Santos"]
    bets = []
    for _ in range(3):  # gera 3 bilhetes de exemplo
        home = random.choice(teams)
        away = random.choice([t for t in teams if t != home])
        line = random.choice(["Over 1.5", "Under 2.5", "Ambas marcam"])
        odd = round(random.uniform(1.50, 2.50), 2)
        bets.append(f"⚽ {home} x {away} | {line} @ {odd}")
    return bets

def generate_basketball_bets():
    teams = ["Lakers", "Bulls", "Heat", "Celtics"]
    bets = []
    for _ in range(2):  # gera 2 bilhetes de exemplo
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
# Rota para gerar bilhetes manualmente
# =========================
@app.route("/run-bets")
def run_bets():
    send_bets()
    return "✅ Bilhetes enviados!"

# =========================
# Main
# =========================
if __name__ == "__main__":
    # Roda localmente se precisar
    send_bets()  # envia ao iniciar
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
