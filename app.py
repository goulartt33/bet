from flask import Flask
from telegram import Bot

# Dados do Telegram
TELEGRAM_TOKEN = "7783572211:AAE99ISsfogVLk4r5fELoKzAVhwB_8okq-c"
CHAT_ID = 5538926378

bot = Bot(token=TELEGRAM_TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot de apostas online ativo!"

@app.route('/run-bets')
def run_bets():
    # Aqui você colocaria sua lógica de geração de bilhetes
    # Exemplo de bilhete fixo
    mensagem = "🏀 Jogo do dia: Atlanta Hawks vs Miami Heat\n📊 Sugestão de aposta: Over 219.5 pontos"
    bot.send_message(chat_id=CHAT_ID, text=mensagem)
    return "Bilhete enviado para o Telegram!"

if __name__ == "__main__":
    app.run(debug=True)
