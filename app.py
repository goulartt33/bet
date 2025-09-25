from flask import Flask, jsonify
from flask_cors import CORS
from football_analysis import generate_football_tickets
from basketball_analysis import generate_basketball_tickets

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "📊 Bot de Apostas Online - Multi-Esporte"

@app.route('/tickets/football')
def football_tickets():
    tickets = generate_football_tickets()
    return jsonify(tickets)

@app.route('/tickets/basketball')
def basketball_tickets():
    tickets = generate_basketball_tickets()
    return jsonify(tickets)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
