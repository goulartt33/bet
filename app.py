from flask import Flask, jsonify
import requests
from telegram import Bot
import datetime

# ==============================
# CONFIGURAÇÕES
# ==============================
TELEGRAM_TOKEN = "7783572211:AAE99ISsfogVLk4r5fELoKzAVhwB_8okq-c"
CHAT_ID = 5538926378
SPORTRADAR_KEY = "0g17DmKKFvqG5IR090twLsDycgb2ZhtgGLWAP3uj"

bot = Bot(token=TELEGRAM_TOKEN)
app = Flask(__name__)

# ==============================
# FUNÇÃO PARA OBTER JOGOS DO DIA (Exemplo NBA)
# ==============================
def get_nba_games_today():
    hoje = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    url = f"https://api.sportradar.us/nba/trial/v7/en/games/{hoje}/schedule.json?api_key={SPORTRADAR_KEY}"
    
    response = requests.get(url)
    if response.status_code != 200:
        return []

    data = response.json()
    jogos = []

    # Percorre os jogos do dia
    for game in data.get("games", []):
        jogo = {
            "home": game["home"]["name"],
            "away": game["away"]["name"],
            "scheduled": game["scheduled"]
        }
        jogos.append(jogo)
    return jogos

# ==============================
# FUNÇÃO PARA GERAR BILHETE
# ==============================
def gerar_bilhete(jogo):
    # Exemplo simples: envia Over/Under fixo
    mensagem = f"🏀 {jogo['home']} vs {jogo['away']} ({jogo['scheduled']})\n"
    mensagem += "📊 Sugestão de aposta:\n"
    mensagem += f"🔢 Total: Over 219.5 pontos @ 1.95\n"
    mensagem += f"🔢 Total: Under 219.5 pontos @ 1.93\n"
    return mensagem

# ==============================
# ROTA PRINCIPAL
# ==============================
@app.route('/')
def index():
    return "Bot de apostas online ativo!"

# ==============================
# ROTA PARA GERAR E ENVIAR BILHETES
# ==============================
@app.route('/run-bets')
def run_bets():
    jogos = get_nba_games_today()
    if not jogos:
        return "Nenhum jogo encontrado hoje."

    mensagens_enviadas = []
    for jogo in jogos:
        bilhete = gerar_bilhete(jogo)
        try:
            bot.send_message(chat_id=CHAT_ID, text=bilhete)
            mensagens_enviadas.append(f"{jogo['home']} vs {jogo['away']}")
        except Exception as e:
            print(f"Erro ao enviar Telegram: {e}")

    return jsonify({
        "status": "ok",
        "jogos_enviados": mensagens_enviadas
    })

# ==============================
# RODAR APP LOCAL
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
