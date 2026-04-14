import streamlit as st
import random

st.set_page_config(page_title="Dream11 AI Guru", layout="wide")

# ================= AI GURU =================
class AdvancedAIGuru:
    def __init__(self):
        self.pitch_report = {
            "venue": "Wankhede Stadium",
            "type": "Batting Paradise",
            "behavior": "High dew. Chasing advantage",
            "avg_score": 198
        }
        self.players = self._load_players()

    def _load_players(self):
        return [
            {'id': 1, 'name': 'Rohit Sharma', 'role': 'BAT', 'team': 'MI', 'points': 780, 'sel': 91, 'ml': 87},
            {'id': 2, 'name': 'Virat Kohli', 'role': 'BAT', 'team': 'MI', 'points': 920, 'sel': 94, 'ml': 94},
            {'id': 3, 'name': 'Jasprit Bumrah', 'role': 'BOWL', 'team': 'MI', 'points': 850, 'sel': 93, 'ml': 93},
            {'id': 4, 'name': 'Ravindra Jadeja', 'role': 'AR', 'team': 'CSK', 'points': 780, 'sel': 92, 'ml': 90},
            {'id': 5, 'name': 'Ruturaj Gaikwad', 'role': 'BAT', 'team': 'CSK', 'points': 680, 'sel': 82, 'ml': 88},
            {'id': 6, 'name': 'Ishan Kishan', 'role': 'WK', 'team': 'MI', 'points': 420, 'sel': 68, 'ml': 82},
        ]

    def generate_cvc(self, team):
        team_sorted = sorted(team, key=lambda x: x['ml'], reverse=True)
        return team_sorted[0], team_sorted[1]

    def detect_pairs(self, team):
        names = [p['name'] for p in team]
        if "Rohit Sharma" in names and "Bumrah" in names:
            return "🔥 Rohit + Bumrah combo strong (70% win rate)"
        if "Jadeja" in names and "Ruturaj Gaikwad" in names:
            return "🔥 Jadeja + Ruturaj combo solid"
        return "No strong pair detected"

guru = AdvancedAIGuru()

# ================= UI =================

st.title("🏏 Dream11 AI Guru (Streamlit Version)")

# Pitch Report
st.subheader("📊 Pitch Report")
st.json(guru.pitch_report)

# Player Selection
st.subheader("👥 Select Your Playing 11")

selected_players = st.multiselect(
    "Choose players",
    guru.players,
    format_func=lambda x: f"{x['name']} ({x['role']}) - ML:{x['ml']}"
)

# Generate C/VC
if st.button("🚀 Generate Captain / Vice Captain"):
    if len(selected_players) < 2:
        st.warning("⚠️ At least 2 players select karo")
    else:
        c, vc = guru.generate_cvc(selected_players)

        st.success(f"🔥 Captain: {c['name']}")
        st.info(f"⚡ Vice Captain: {vc['name']}")

        # Pair Insight
        st.subheader("🤝 Pair Insight")
        st.write(guru.detect_pairs(selected_players))

        # Differential Pick
        low_sel = [p for p in selected_players if p['sel'] < 75]
        if low_sel:
            diff = random.choice(low_sel)
            st.warning(f"💣 Differential Pick: {diff['name']} ({diff['sel']}% selection)")
