# app.py
from flask import Flask, jsonify
from flask_cors import CORS
import requests
import datetime
import os
from telegram import Bot

# Configurações do Telegram
TELEGRAM_TOKEN = "7783572211:AAE99ISsfogVLk4r5fELoKzAVhwB_8okq-c"
TELEGRAM_CHAT_ID = "5538926378"
bot = Bot(token=TELEGRAM_TOKEN)

# Configurações APIs
SPORT_RADAR_API_KEY = "0g17DmKKFvqG5IR090twLsDycgb2ZhtgGLWAP3uj"
BALDONTLIE_API_URL = "https://www.balldontlie.io/api/v1"

app = Flask(__name__)
CORS(app)

# Função para buscar jogos de futebol via SportRadar
def get_football_games(days=5):
    games = []
    today = datetime.date.today()
    for i in range(days):
        date = (today + datetime.timedelta(days=i)).isoformat()
        url = f"https://api.sportradar.com/soccer/trial/v4/en/schedules/{date}/schedule.json?api_key={SPORT_RADAR_API_KEY}"
        try:
            resp = requests.get(url)
            data = resp.json()
            if "sport_events" in data:
                for match in data["sport_events"]:
                    games.append({
                        "type": "futebol",
                        "date": match.get("scheduled"),
                        "home": match["competitors"][0]["name"],
                        "away": match["competitors"][1]["name"],
                        "league": match["tournament"]["name"],
                        "id": match["id"]
                    })
        except Exception as e:
            print("Erro Futebol:", e)
    return games

# Função para buscar jogos de basquete via balldontlie
def get_basketball_games(days=5):
    games = []
    today = datetime.date.today()
    end_date = today + datetime.timedelta(days=days)
    url = f"{BALDONTLIE_API_URL}/games?start_date={today}&end_date={end_date}"
    try:
        resp = requests.get(url)
        data = resp.json()
        for game in data['data']:
            games.append({
                "type": "basquete",
                "date": game["date"],
                "home": game["home_team"]["full_name"],
                "away": game["visitor_team"]["full_name"],
                "home_score": game["home_team_score"],
                "away_score": game["visitor_team_score"]
            })
    except Exception as e:
        print("Erro Basquete:", e)
    return games

# Função para enviar mensagem no Telegram
def send_telegram_message(message):
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception as e:
        print("Erro Telegram:", e)

# Função para montar mensagem de futebol
def format_football_message(match):
    return f"⚽ {match['home']} vs {match['away']} ({match['date']})\n🏆 {match['league']}"

# Função para montar mensagem de basquete
def format_basketball_message(match):
    return f"🏀 {match['home']} vs {match['away']} ({match['date']})\nScore: {match['home_score']} - {match['away_score']}"

# Endpoint principal
@app.route("/send_games", methods=["GET"])
def send_games():
    football_games = get_football_games()
    basketball_games = get_basketball_games()

    if not football_games and not basketball_games:
        return jsonify({"message": "Nenhum jogo encontrado para os próximos 5 dias."})

    for match in football_games:
        msg = format_football_message(match)
        send_telegram_message(msg)

    for match in basketball_games:
        msg = format_basketball_message(match)
        send_telegram_message(msg)

    return jsonify({"message": "Jogos enviados para o Telegram com sucesso!"})

# Endpoint raiz
@app.route("/", methods=["GET"])
def index():
    return "Bot de esportes funcionando!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
