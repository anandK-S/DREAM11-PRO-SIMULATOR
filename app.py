from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import random

app = Flask(__name__)
app.secret_key = "dream11_ultimate_ai_2026"
socketio = SocketIO(app, cors_allowed_origins="*")

class AdvancedAIGuru:
    def __init__(self):
        self.pitch_report = {
            "venue": "Wankhede Stadium",
            "type": "Red Soil Batting Paradise",
            "behavior": "High dew factor. 2nd innings 85% win rate. Target: 200+",
            "avg_score": 198,
            "toss_winner": "CSK (Batting 2nd)"
        }
        self.players = self._load_players()
        self.pair_analysis = self._analyze_pairs()

    def _load_players(self):
        return [
            {'id': 1, 'name': 'Rohit Sharma', 'role': 'BAT', 'team': 'MI', 'credits': 9.5, 'points': 780, 'sel': '91%', 'ml_score': 87},
            {'id': 2, 'name': 'Virat Kohli', 'role': 'BAT', 'team': 'MI', 'credits': 10.0, 'points': 920, 'sel': '94%', 'ml_score': 94},
            {'id': 3, 'name': 'Jasprit Bumrah', 'role': 'BOWL', 'team': 'MI', 'credits': 9.5, 'points': 850, 'sel': '93%', 'ml_score': 93},
            {'id': 4, 'name': 'Ravindra Jadeja', 'role': 'AR', 'team': 'CSK', 'credits': 9.0, 'points': 780, 'sel': '92%', 'ml_score': 90},
            {'id': 5, 'name': 'Ruturaj', 'role': 'BAT', 'team': 'CSK', 'credits': 9.0, 'points': 680, 'sel': '82%', 'ml_score': 88},
        ]

    def _analyze_pairs(self):
        return {
            ('Rohit Sharma', 'Jasprit Bumrah'): {'avg_pts': 150, 'win_rate': 70},
            ('Ravindra Jadeja', 'Ruturaj'): {'avg_pts': 158, 'win_rate': 68},
        }

    def generate_cvc(self, team):
        sorted_team = sorted(team, key=lambda x: x['ml_score'], reverse=True)
        return {
            "captain": sorted_team[0]['name'],
            "vice_captain": sorted_team[1]['name']
        }

guru = AdvancedAIGuru()

@app.route('/')
def home():
    return "Dream11 AI Backend Running 🚀"

@app.route('/api/data')
def data():
    return jsonify({
        "players": guru.players,
        "pitch": guru.pitch_report
    })

@app.route('/api/cvc', methods=['POST'])
def cvc():
    team = request.json.get("team", [])
    return jsonify(guru.generate_cvc(team))

# ✅ FIXED RUN LINE
if __name__ == '__main__':
    socketio.run(
        app,
        host='0.0.0.0',
        port=5005,
        debug=True,
        allow_unsafe_werkzeug=True
    )
