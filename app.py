import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random

# --- CONFIG ---
st.set_page_config(page_title="Dream11 AI Guru Pro", layout="wide")

# --- ADVANCED AI LOGIC (Aapka logic, Streamlit style mein) ---
class AdvancedAIGuru:
    def __init__(self):
        self.pitch_report = {
            "venue": "Wankhede Stadium", 
            "type": "Red Soil Batting Paradise",
            "behavior": "High dew factor. 2nd innings 85% win rate. Target: 200+",
            "avg_score": 198
        }
        self.players = self._load_players()
        self.pair_analysis = {
            ('Rohit Sharma', 'Sky'): {'avg_pts': 165, 'win_rate': 72},
            ('Jadeja', 'Ruturaj'): {'avg_pts': 158, 'win_rate': 68},
            ('Virat Kohli', 'Maxwell'): {'avg_pts': 172, 'win_rate': 75},
        }

    def _load_players(self):
        return [
            {'id': 1, 'name': 'Ishan Kishan', 'role': 'WK', 'team': 'MI', 'credits': 8.5, 'points': 420, 'sel': '68%', 'radar': [78, 82, 65, 55, 88], 'ml_score': 82},
            {'id': 2, 'name': 'Virat Kohli', 'role': 'BAT', 'team': 'MI', 'credits': 10.0, 'points': 920, 'sel': '94%', 'radar': [97, 88, 92, 87, 96], 'ml_score': 94},
            {'id': 3, 'name': 'Rohit Sharma', 'role': 'BAT', 'team': 'MI', 'credits': 9.5, 'points': 780, 'sel': '91%', 'radar': [85, 92, 78, 75, 89], 'ml_score': 87},
            {'id': 6, 'name': 'Jasprit Bumrah', 'role': 'BOWL', 'team': 'MI', 'credits': 9.5, 'points': 850, 'sel': '93%', 'radar': [94, 72, 98, 92, 91], 'ml_score': 93},
            {'id': 13, 'name': 'Ravindra Jadeja', 'role': 'AR', 'team': 'CSK', 'credits': 9.0, 'points': 780, 'sel': '92%', 'radar': [89, 82, 94, 88, 85], 'ml_score': 90},
        ]

    def get_cvc_recommendation(self, team):
        if not team: return None
        high_ml = sorted(team, key=lambda x: x['ml_score'], reverse=True)
        return {
            'safe': f"**Safe:** {high_ml[0]['name']} (C) + {high_ml[1]['name']} (VC)",
            'ml_score': high_ml[0]['ml_score']
        }

# Initialize AI
if 'guru' not in st.session_state:
    st.session_state.guru = AdvancedAIGuru()
if 'my_team' not in st.session_state:
    st.session_state.my_team = []

guru = st.session_state.guru

# --- UI DESIGN ---
st.title("💎 Dream11 AI Guru Pro Simulator")

col1, col2, col3 = st.columns([1, 2, 1])

# Column 1: Match Info
with col1:
    st.header("🏟️ Match Info")
    st.success(f"**Venue:** {guru.pitch_report['venue']}")
    st.info(f"**Pitch:** {guru.pitch_report['type']}\n\n{guru.pitch_report['behavior']}")
    
    st.subheader("🔥 Live Trends")
    st.write("📈 **Trending C:** Rohit Sharma")
    st.write("🔥 **Hot Pair:** Rohit + Sky")

# Column 2: Squad Builder
with col2:
    st.header("🏏 Select Your 11")
    credits_used = sum(p['credits'] for p in st.session_state.my_team)
    st.write(f"**Players:** {len(st.session_state.my_team)}/11 | **Credits Left:** {100 - credits_used}")
    
    # Filter by role
    role = st.selectbox("Filter Role", ["WK", "BAT", "AR", "BOWL"])
    role_players = [p for p in guru.players if p['role'] == role]
    
    for p in role_players:
        selected = any(t['id'] == p['id'] for t in st.session_state.my_team)
        col_p1, col_p2, col_p3 = st.columns([3, 1, 1])
        col_p1.write(f"**{p['name']}** ({p['team']})")
        col_p2.write(f"{p['credits']} Cr")
        if selected:
            if col_p3.button("Remove", key=f"rem_{p['id']}"):
                st.session_state.my_team = [t for t in st.session_state.my_team if t['id'] != p['id']]
                st.rerun()
        else:
            if col_p3.button("Add", key=f"add_{p['id']}"):
                if len(st.session_state.my_team) < 11:
                    st.session_state.my_team.append(p)
                    st.rerun()

# Column 3: AI Analysis
with col3:
    st.header("🧠 AI Analysis")
    if not st.session_state.my_team:
        st.write("Add players to see radar analysis.")
    else:
        # Show radar for last selected player
        p = st.session_state.my_team[-1]
        st.subheader(f"Player Profile: {p['name']}")
        
        categories = ['Form', 'Consistency', 'Matchup', 'Venue', 'Skill']
        fig = go.Figure(data=go.Scatterpolar(
            r=p['radar'],
            theta=categories,
            fill='toself',
            line_color='purple'
        ))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # C/VC Recommendations
        if len(st.session_state.my_team) >= 2:
            reco = guru.get_cvc_recommendation(st.session_state.my_team)
            st.warning(reco['safe'])
            st.metric("Win Probability", f"{reco['ml_score']}%")
