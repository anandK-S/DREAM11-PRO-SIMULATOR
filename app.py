import streamlit as st
import random

st.set_page_config(page_title="Dream11 AI Guru", layout="wide")

class AIGuru:
    def __init__(self):
        self.players = [
            {"name": "Rohit Sharma", "role": "BAT", "points": 780, "sel": 91, "ml": 87},
            {"name": "Virat Kohli", "role": "BAT", "points": 920, "sel": 94, "ml": 94},
            {"name": "Bumrah", "role": "BOWL", "points": 850, "sel": 93, "ml": 93},
            {"name": "Jadeja", "role": "AR", "points": 780, "sel": 92, "ml": 90},
            {"name": "Ruturaj", "role": "BAT", "points": 680, "sel": 82, "ml": 88},
        ]

    def get_best_cvc(self, team):
        team_sorted = sorted(team, key=lambda x: x["ml"], reverse=True)
        return team_sorted[0]["name"], team_sorted[1]["name"]

guru = AIGuru()

st.title("🏏 Dream11 AI Team Generator")

selected = st.multiselect(
    "Select Players",
    guru.players,
    format_func=lambda x: f"{x['name']} ({x['role']})"
)

if st.button("Generate C/VC"):
    if len(selected) < 2:
        st.warning("Select at least 2 players")
    else:
        c, vc = guru.get_best_cvc(selected)
        st.success(f"🔥 Captain: {c}")
        st.info(f"⚡ Vice Captain: {vc}")
