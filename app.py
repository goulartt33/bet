from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # permite que qualquer frontend acesse a API

@app.route("/")
def home():
    return "✅ Bot de Apostas online no Render!"

@app.route("/odds")
def odds():
    # Aqui você pode colocar os dados reais ou simulados
    return jsonify({
        "match": "Team A vs Team B",
        "markets": [
            {"type": "1x2", "odds": {"1": 2.1, "X": 3.2, "2": 3.5}},
            {"type": "over/under", "odds": {"over 2.5": 1.9, "under 2.5": 1.95}}
        ]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
