import streamlit as st
import streamlit.components.v1 as components

# Streamlit Page Configuration (Wide layout)
st.set_page_config(page_title="Dream11 Pro Simulator", layout="wide", initial_sidebar_state="collapsed")

# 1. FIX TOP SPACING & REMOVE STREAMLIT DEFAULT UI
remove_st_spacing = """
<style>
    /* Remove top padding and max-width */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    /* Hide Header, MainMenu, and Footer */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* Remove iframe border */
    iframe {
        border: none !important;
        width: 100% !important;
    }
</style>
"""
st.markdown(remove_st_spacing, unsafe_allow_html=True)

# 2. FULL RESPONSIVE HTML/CSS/JS CODE (FIXED DESKTOP HEIGHT)
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Dream11 Ultimate Pro Simulator</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    
    <style>
        :root { 
            --bg-color: #f1f5f9; --white: #ffffff; 
            --d11-red: #d32f2f; --d11-green: #10b981; --d11-orange: #f97316;
            --mi-blue: #2563eb; --csk-yellow: #eab308; --rcb-red: #ef4444;
            --text-main: #1e293b; --text-muted: #64748b;
            --border: #e2e8f0; --shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background-color: var(--bg-color); font-family: 'Roboto', sans-serif; padding: 20px; color: var(--text-main); overflow-x: hidden; }
        h1, h2, h3, h4 { font-family: 'Outfit', sans-serif; }
        ::-webkit-scrollbar { width: 4px; } ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }

        .header { 
            background: var(--white); padding: 15px 20px; border-radius: 16px; margin-bottom: 20px; 
            box-shadow: var(--shadow); text-align: center;
        }
        .header h1 { font-weight: 800; font-size: 24px; color: var(--d11-red); text-transform: uppercase; letter-spacing: 1px; margin: 0; }
        .match-status { font-size: 13px; color: var(--text-muted); margin-top: 5px; }

        /* --- RESPONSIVE GRID LAYOUT (FIXED FOR DESKTOP) --- */
        .dashboard { 
            display: grid; 
            grid-template-columns: 300px 1fr 320px; 
            gap: 20px; 
            /* Fixed height for Desktop to prevent bottom buttons from stretching too far down */
            height: 720px; 
        }
        
        .panel { background: var(--white); border-radius: 20px; padding: 20px; box-shadow: var(--shadow); overflow-y: auto; height: 100%; }
        .panel-title { font-size: 15px; font-weight: 800; color: var(--text-main); margin-bottom: 15px; 
                       display: flex; align-items: center; gap: 8px; border-bottom: 1px solid var(--border); 
                       padding-bottom: 10px;}

        /* APP FRAME */
        .app-frame { border-radius: 24px; border: 6px solid #cbd5e1; background: var(--white); 
                     height: 100%; position: relative; overflow: hidden; box-shadow: 0 15px 25px -5px rgba(0,0,0,0.1); }
        .screen { width: 100%; height: 100%; position: absolute; top: 0; left: 0; 
                  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1); display: flex; flex-direction: column; }
        
        #screen-builder { transform: translateX(0); }
        #screen-cvc { transform: translateX(100%); background: #f8fafc; }
        #screen-preview { transform: translateX(100%); background: #1e293b; }

        .app-header { background: #0f172a; color: white; padding: 12px 15px; 
                      display: flex; justify-content: space-between; align-items: center;}
        .team-code { font-family: 'Outfit'; font-weight: 800; font-size: 16px; }
        
        /* Auto Swap Alert */
        .swap-alert { background: #fee2e2; border-bottom: 1px solid #fca5a5; padding: 10px 15px; 
                      display: none; align-items: center; justify-content: space-between; font-size: 12px; }
        .btn-swap { background: var(--d11-red); color: white; border: none; padding: 6px 12px; 
                    border-radius: 6px; cursor: pointer; font-family: 'Outfit'; font-weight: 600; font-size: 12px; }

        .tabs { display: flex; border-bottom: 1px solid var(--border); }
        .tab { flex: 1; text-align: center; padding: 10px 0; cursor: pointer; font-weight: 600; 
               color: var(--text-muted); font-size: 13px; border-bottom: 3px solid transparent;}
        .tab.active { color: var(--d11-red); border-color: var(--d11-red); }
        
        .player-list-area { flex: 1; overflow-y: auto; padding-bottom: 70px; }
        
        .player-row { display: flex; justify-content: space-between; align-items: center; 
                      padding: 12px 15px; border-bottom: 1px solid #f1f5f9; cursor: pointer; 
                      transition: 0.2s; position: relative; }
        .player-row:hover { background: #f8fafc; }
        .player-row.selected { background: #ecfdf5; border-left: 4px solid var(--d11-green); }
        
        .playing-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; 
                       margin-right: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
        .playing-dot.yes { background: var(--d11-green); animation: pulse 2s infinite; }
        .playing-dot.no { background: var(--d11-red); }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.7; } }

        .p-main { display: flex; align-items: center; gap: 10px; flex: 1; }
        .p-img { width: 36px; height: 36px; border-radius: 8px; background: linear-gradient(135deg, var(--mi-blue), var(--csk-yellow)); 
                 display: flex; justify-content: center; align-items: center; color: white; font-weight: bold; font-size: 12px; }
        .p-name { font-weight: 700; font-size: 14px; font-family: 'Outfit'; }
        .p-sub { font-size: 10px; color: var(--text-muted); }
        
        .btn-add { width: 24px; height: 24px; border-radius: 50%; border: 2px solid var(--d11-green); 
                   color: var(--d11-green); display: flex; justify-content: center; align-items: center; 
                   font-weight: bold; cursor: pointer; transition: 0.2s; font-size: 14px; }
        .player-row.selected .btn-add { background: var(--d11-green); color: white; }

        .ai-suggest { position: absolute; top: 8px; right: 12px; background: var(--d11-orange); 
                      color: white; padding: 3px 6px; border-radius: 10px; font-size: 9px; 
                      font-weight: 800; animation: bounce 2s infinite; }
        @keyframes bounce { 0%, 20%, 50%, 80%, 100% { transform: translateY(0); } 
                           40% { transform: translateY(-4px); } 60% { transform: translateY(-2px); } }

        .cvc-header { background: #fff8e1; color: #b45309; padding: 10px; text-align: center; 
                      font-size: 11px; font-weight: 600; }
        .cvc-row { background: var(--white); margin: 8px 12px; padding: 12px; border-radius: 12px; 
                   border: 1px solid var(--border); display: flex; justify-content: space-between; 
                   align-items: center; cursor: pointer; transition: 0.2s; }
        .cvc-row:hover { background: #f8fafc; }
        .circle-btn { width: 34px; height: 34px; border-radius: 50%; border: 2px solid #cbd5e1; 
                      color: #94a3b8; font-weight: 800; cursor: pointer; transition: 0.2s; display: flex; align-items: center; justify-content: center; font-size: 12px;}
        .circle-btn.c-active { background: #1e293b; border-color: #1e293b; color: #fbbf24; transform: scale(1.1); }
        .circle-btn.vc-active { background: #64748b; border-color: #64748b; color: white; transform: scale(1.1); }

        .cricket-pitch { flex: 1; background: linear-gradient(#4ade80 0%, #22c55e 50%, #16a34a 100%); 
                         display: flex; flex-direction: column; justify-content: space-around; padding: 15px 0; overflow-y: auto;}
        .pitch-role-row { display: flex; justify-content: center; flex-wrap: wrap; gap: 8px; padding: 5px 0; }
        .pitch-player { text-align: center; position: relative; width: 55px; }
        .pitch-player img { width: 38px; height: 38px; border-radius: 50%; border: 2px solid white; 
                            box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
        .pitch-player .p-name { background: rgba(0,0,0,0.8); color: white; font-size: 9px; 
                                padding: 2px 4px; border-radius: 8px; margin-top: -6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;}
        .pitch-player .pts { color: white; font-size: 10px; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.8); }
        .badge-c { position: absolute; top: -3px; right: -3px; background: #fbbf24; color: black; 
                   font-size: 8px; font-weight: 900; width: 14px; height: 14px; border-radius: 50%; 
                   display: flex; align-items: center; justify-content: center; border: 1px solid black; }

        .bottom-bar { position: absolute; bottom: 0; left: 0; width: 100%; background: var(--white); 
                      padding: 12px; border-top: 1px solid var(--border); z-index: 10;}
        .btn-primary { width: 100%; background: #e2e8f0; color: #94a3b8; border: none; 
                       padding: 12px; border-radius: 30px; font-family: 'Outfit'; font-weight: 800; 
                       font-size: 14px; transition: 0.3s; cursor: not-allowed; }
        .btn-primary.ready { background: var(--d11-green); color: white; cursor: pointer; box-shadow: 0 10px 15px rgba(16,185,129,0.3); }

        .dv-container { width: 100%; height: 240px; margin-top: 10px; }
        .ai-insight-box { background: linear-gradient(135deg, #f8fafc, #e2e8f0); border: 1px solid var(--border); 
                          padding: 12px; border-radius: 12px; margin-bottom: 12px; border-left: 4px solid #8b5cf6; }
        .pair-suggestion { background: #ecfdf5; border: 1px solid var(--d11-green); padding: 10px; 
                           border-radius: 10px; margin-top: 10px; font-size: 12px; }

        /* --- MOBILE VIEW CSS --- */
        @media (max-width: 992px) {
            .dashboard {
                display: flex;
                flex-direction: column;
                height: auto; /* Let it expand freely on mobile */
                gap: 15px;
            }
            .app-frame {
                height: 650px; /* Specific height for mobile phone feel */
                border-width: 4px;
            }
            .panel {
                height: auto;
            }
            .dv-container { height: 280px; }
            .header h1 { font-size: 20px; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1><i class="fas fa-crown"></i> DREAM11 PRO SIMULATOR</h1>
        <div class="match-status" id="matchStatus">MI vs CSK • Wankhede • Lineups Pending</div>
    </div>

    <div class="dashboard">
        <div class="panel">
            <div class="panel-title"><i class="fas fa-layer-group" style="color: var(--d11-red)"></i> Match Intelligence</div>
            <div style="background: #fffbeb; border: 1px solid #fde68a; padding: 12px; border-radius: 12px; margin-bottom: 15px;">
                <div id="pitchText" style="font-size: 12px; color: #92400e; font-weight: 500;">Loading Pitch Report...</div>
            </div>
            <div class="panel-title"><i class="fas fa-bullhorn" style="color: var(--d11-orange)"></i> Live Updates</div>
            <button onclick="announceLineups()" style="width:100%; padding: 12px; background: linear-gradient(135deg, var(--d11-orange), #ea580c); 
                              color: white; border:none; border-radius:12px; cursor:pointer; font-weight:700; margin-bottom:10px; font-size: 13px;">
                <i class="fas fa-sync-alt"></i> ANNOUNCE LINEUPS
            </button>
            <div id="lineupStatus" style="font-size:11px; color:var(--text-muted); text-align:center;">Click to simulate 7:00 PM toss & playing XI</div>
        </div>

        <div class="panel" style="padding: 0; background: transparent; box-shadow: none;">
            <div class="app-frame">
                <div id="screen-builder" class="screen">
                    <div class="app-header">
                        <div class="team-code">MI vs CSK • 100 Cr</div>
                        <div style="font-size: 11px; color: #94a3b8;">Max 10/Team</div>
                    </div>
                    
                    <div class="swap-alert" id="swapAlert">
                        <div><i class="fas fa-exclamation-triangle" style="color:var(--d11-red)"></i> 
                             <span style="font-weight:600;">Benched players!</span></div>
                        <button class="btn-swap" onclick="autoSwapAI()"><i class="fas fa-magic"></i> AI Fix</button>
                    </div>

                    <div style="padding: 12px 15px; background: #f8fafc; display: flex; justify-content: space-between; 
                                border-bottom: 1px solid var(--border);">
                        <div><div style="font-size: 20px; font-family: 'Outfit'; font-weight: 900;" id="playerCount">0/11</div>
                             <div style="font-size: 10px; font-weight: bold; color: var(--text-muted);">PLAYERS</div></div>
                        <div style="text-align: right;">
                            <div style="font-size: 20px; font-family: 'Outfit'; font-weight: 900;" id="creditCount">100.0</div>
                            <div style="font-size: 10px; font-weight: bold; color: var(--text-muted);">CREDITS LEFT</div></div>
                    </div>
                    
                    <div class="tabs">
                        <div class="tab active" onclick="switchTab('WK')">WK</div>
                        <div class="tab" onclick="switchTab('BAT')">BAT</div>
                        <div class="tab" onclick="switchTab('AR')">AR</div>
                        <div class="tab" onclick="switchTab('BOWL')">BOWL</div>
                    </div>
                    <div class="player-list-area" id="playerListArea"></div>
                    <div class="bottom-bar">
                        <button class="btn-primary" id="btnNext" onclick="goToCVC()">NEXT: C/VC Selection</button>
                    </div>
                </div>

                <div id="screen-cvc" class="screen">
                    <div class="app-header" onclick="goToBuilder()" style="cursor:pointer;">
                        <div><i class="fas fa-arrow-left"></i> Edit</div>
                        <div class="team-code">Captain/VC</div>
                    </div>
                    <div class="cvc-header">
                        <i class="fas fa-star"></i> C = 2X | VC = 1.5X | AI Optimized
                    </div>
                    <div class="player-list-area" id="cvcListArea" style="background: #f8fafc;"></div>
                    <div class="bottom-bar">
                        <button class="btn-primary ready" id="btnPreview" onclick="goToPreview()">PREVIEW TEAM</button>
                    </div>
                </div>

                <div id="screen-preview" class="screen">
                    <div class="app-header" onclick="backToCVC()" style="cursor:pointer;">
                        <div><i class="fas fa-edit"></i> Edit</div>
                        <div class="team-code">Final Preview</div>
                    </div>
                    <div class="cricket-pitch" id="pitchPreview"></div>
                    <div style="background: rgba(15,23,42,0.95); color: white; text-align: center; padding: 15px; 
                                font-family: 'Outfit'; font-weight: 800; border-top: 2px solid var(--d11-gold);">
                        AI PROJECTED: <span style="color:var(--d11-green); font-size:20px;" id="totalPoints">0</span> PTS
                        <br><span style="font-size:11px; opacity:0.9;">Top 1% Grand League Potential</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="panel">
            <div class="panel-title"><i class="fas fa-brain" style="color: #8b5cf6;"></i> AI Match Predictor</div>
            <div id="aiPanel">
                <div style="text-align: center; color: var(--text-muted); margin-top: 40px; font-size: 13px;">
                    <i class="fas fa-robot fa-2x" style="margin-bottom: 12px; color: #cbd5e1;"></i>
                    <div style="font-family: 'Outfit'; font-weight: 700;">Select players for AI analysis</div>
                    <div style="font-size: 11px; margin-top: 5px;">Pair synergy • Floor/Ceiling</div>
                </div>
            </div>
            <div id="aiSuggestions" style="display: none; margin-top: 15px;"></div>
        </div>
    </div>

    <script>
        const allPlayersData = [
            // MI - WicketKeepers
            {id:1, name:'Ishan Kishan', role:'WK', team:'MI', credits:8.5, points:420, sel:'68%', is_playing:true, 
             radar:[78,82,68,72,85], floor:45, ceil:120, pair_suggest:['Rohit Sharma', 'Suryakumar Yadav'], ml_score:84},
            {id:2, name:'Tilak Varma', role:'WK', team:'MI', credits:7.5, points:320, sel:'42%', is_playing:false, 
             radar:[65,70,62,58,72], floor:30, ceil:95, pair_suggest:['Rohit Sharma'], ml_score:72},
            
            // MI - Batsmen
            {id:3, name:'Rohit Sharma', role:'BAT', team:'MI', credits:9.5, points:780, sel:'92%', is_playing:true, 
             radar:[88,92,82,85,90], floor:65, ceil:160, pair_suggest:['Suryakumar Yadav', 'Ishan Kishan'], ml_score:91},
            {id:4, name:'Suryakumar Yadav', role:'BAT', team:'MI', credits:9.0, points:720, sel:'88%', is_playing:true, 
             radar:[92,88,95,78,88], floor:70, ceil:155, pair_suggest:['Rohit Sharma', 'Tilak Varma'], ml_score:89},
            {id:5, name:'Tilak Varma', role:'BAT', team:'MI', credits:8.0, points:450, sel:'75%', is_playing:true, 
             radar:[75,78,72,68,80], floor:40, ceil:110, pair_suggest:['Suryakumar Yadav'], ml_score:78},
            {id:6, name:'Nehal Wadhera', role:'BAT', team:'MI', credits:7.0, points:280, sel:'35%', is_playing:false, 
             radar:[62,65,58,55,68], floor:25, ceil:85, pair_suggest:[], ml_score:65},
            
            // MI - All Rounders  
            {id:7, name:'Hardik Pandya', role:'AR', team:'MI', credits:9.0, points:650, sel:'85%', is_playing:true, 
             radar:[82,85,88,80,82], floor:55, ceil:140, pair_suggest:['Jasprit Bumrah'], ml_score:87},
            {id:8, name:'Romario Shepherd', role:'AR', team:'MI', credits:7.5, points:380, sel:'45%', is_playing:true, 
             radar:[70,72,75,65,75], floor:35, ceil:100, pair_suggest:['Hardik Pandya'], ml_score:74},
            
            // MI - Bowlers
            {id:9, name:'Jasprit Bumrah', role:'BOWL', team:'MI', credits:9.5, points:850, sel:'95%', is_playing:true, 
             radar:[95,88,98,92,94], floor:75, ceil:170, pair_suggest:['Rohit Sharma', 'Hardik Pandya'], ml_score:95},
            {id:10, name:'Gerald Coetzee', role:'BOWL', team:'MI', credits:8.0, points:480, sel:'65%', is_playing:true, 
             radar:[78,75,85,78,80], floor:45, ceil:115, pair_suggest:['Jasprit Bumrah'], ml_score:81},
            {id:11, name:'Piyush Chawla', role:'BOWL', team:'MI', credits:7.5, points:350, sel:'52%', is_playing:false, 
             radar:[68,70,72,65,70], floor:30, ceil:90, pair_suggest:[], ml_score:69},
            
            // CSK - WicketKeepers
            {id:12, name:'MS Dhoni', role:'WK', team:'CSK', credits:8.0, points:380, sel:'78%', is_playing:true, 
             radar:[72,85,55,68,92], floor:40, ceil:105, pair_suggest:['Ravindra Jadeja'], ml_score:80},
            {id:13, name:'Devon Conway', role:'WK', team:'CSK', credits:8.5, points:520, sel:'72%', is_playing:true, 
             radar:[80,78,75,72,82], floor:50, ceil:125, pair_suggest:['Ruturaj Gaikwad'], ml_score:83},
            
            // CSK - Batsmen
            {id:14, name:'Ruturaj Gaikwad', role:'BAT', team:'CSK', credits:9.0, points:680, sel:'87%', is_playing:true, 
             radar:[85,82,88,80,85], floor:60, ceil:145, pair_suggest:['Ravindra Jadeja', 'Devon Conway'], ml_score:88},
            {id:15, name:'Shivam Dube', role:'BAT', team:'CSK', credits:8.5, points:580, sel:'80%', is_playing:true, 
             radar:[82,88,85,75,82], floor:55, ceil:135, pair_suggest:['Ravindra Jadeja'], ml_score:85},
            {id:16, name:'Rajat Patidar', role:'BAT', team:'CSK', credits:7.5, points:420, sel:'58%', is_playing:false, 
             radar:[70,72,68,62,75], floor:35, ceil:100, pair_suggest:[], ml_score:73},
            
            // CSK - All Rounders
            {id:17, name:'Ravindra Jadeja', role:'AR', team:'CSK', credits:9.0, points:780, sel:'93%', is_playing:true, 
             radar:[90,88,92,88,90], floor:70, ceil:160, pair_suggest:['Ruturaj Gaikwad', 'MS Dhoni'], ml_score:93},
            {id:18, name:'Moeen Ali', role:'AR', team:'CSK', credits:8.0, points:450, sel:'62%', is_playing:true, 
             radar:[75,78,72,70,78], floor:40, ceil:110, pair_suggest:['Ravindra Jadeja'], ml_score:77},
            
            // CSK - Bowlers
            {id:19, name:'Matheesha Pathirana', role:'BOWL', team:'CSK', credits:8.5, points:690, sel:'82%', is_playing:true, 
             radar:[88,75,95,85,82], floor:60, ceil:145, pair_suggest:['Ravindra Jadeja'], ml_score:86},
            {id:20, name:'Deepak Chahar', role:'BOWL', team:'CSK', credits:8.0, points:480, sel:'68%', is_playing:true, 
             radar:[78,72,82,78,80], floor:45, ceil:115, pair_suggest:[], ml_score:79},
            {id:21, name:'Tushar Deshpande', role:'BOWL', team:'CSK', credits:7.5, points:380, sel:'55%', is_playing:false, 
             radar:[68,65,75,70,72], floor:35, ceil:95, pair_suggest:[], ml_score:71},
            
            // EXTRA PLAYERS
            {id:22, name:'Tim David', role:'BAT', team:'MI', credits:8.0, points:520, sel:'70%', is_playing:true, radar:[82,85,88,72,80], floor:50, ceil:130, pair_suggest:['Suryakumar Yadav'], ml_score:82},
            {id:23, name:'Akash Madhwal', role:'BOWL', team:'MI', credits:7.0, points:320, sel:'48%', is_playing:true, radar:[65,68,72,65,70], floor:30, ceil:90, pair_suggest:[], ml_score:67},
            {id:24, name:'Ajinkya Rahane', role:'BAT', team:'CSK', credits:7.5, points:380, sel:'60%', is_playing:false, radar:[70,75,65,68,72], floor:35, ceil:100, pair_suggest:[], ml_score:74},
            {id:25, name:'Mitchell Santner', role:'AR', team:'CSK', credits:7.5, points:420, sel:'52%', is_playing:true, radar:[72,75,70,72,75], floor:40, ceil:105, pair_suggest:['Ravindra Jadeja'], ml_score:76},
            {id:26, name:'Shreyas Gopal', role:'BOWL', team:'MI', credits:6.5, points:280, sel:'35%', is_playing:false, radar:[60,62,65,58,65], floor:25, ceil:80, pair_suggest:[], ml_score:62},
            {id:27, name:'Vijay Shankar', role:'AR', team:'CSK', credits:7.0, points:320, sel:'42%', is_playing:false, radar:[65,68,62,60,68], floor:30, ceil:85, pair_suggest:[], ml_score:68},
            {id:28, name:'Karn Sharma', role:'BOWL', team:'MI', credits:6.5, points:260, sel:'28%', is_playing:false, radar:[58,60,62,55,62], floor:22, ceil:75, pair_suggest:[], ml_score:60},
            {id:29, name:'Rachin Ravindra', role:'AR', team:'CSK', credits:7.5, points:380, sel:'50%', is_playing:true, radar:[70,72,68,65,75], floor:35, ceil:100, pair_suggest:['Ruturaj Gaikwad'], ml_score:75},
            {id:30, name:'Naman Dhir', role:'AR', team:'MI', credits:6.5, points:280, sel:'32%', is_playing:true, radar:[62,65,60,58,68], floor:25, ceil:80, pair_suggest:[], ml_score:64}
        ];

        let allPlayers = [], myTeam = [], currentTab = 'WK', creditsLeft = 100.0;
        let selectedC = null, selectedVC = null, lineupsAnnounced = false;

        window.onload = () => {
            allPlayers = [...allPlayersData];
            document.getElementById('pitchText').innerHTML = `
                <b>Red Soil Paradise</b><br>High dew expected. Chasing favored.<br>
                <br><b>Avg Score:</b> 198 | <b>Toss:</b> CSK (Bat 2nd)
            `;
            renderPlayers();
        };

        function switchTab(role) {
            currentTab = role;
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            event.target.classList.add('active');
            renderPlayers();
        }

        function renderPlayers() {
            const listArea = document.getElementById('playerListArea');
            listArea.innerHTML = '';
            
            allPlayers.filter(p => p.role === currentTab).slice(0, 8).forEach(p => {
                const isSelected = myTeam.some(t => t.id === p.id);
                const playingDot = p.is_playing ? 'yes' : 'no';
                const teamColor = p.team === 'MI' ? 'var(--mi-blue)' : p.team === 'CSK' ? 'var(--csk-yellow)' : 'var(--rcb-red)';
                
                const aiSuggest = myTeam.some(t => p.pair_suggest.includes(t.name)) ? 
                    `<div class="ai-suggest">🔥 PAIR</div>` : '';

                listArea.innerHTML += `
                    <div class="player-row ${isSelected ? 'selected' : ''}" onclick="togglePlayer(${p.id})">
                        <div class="p-main">
                            <div class="p-img" style="background: linear-gradient(135deg, ${teamColor}, ${teamColor}88)">
                                ${p.name.split(' ')[0][0]}${p.name.split(' ')[1]?.[0] || ''}
                            </div>
                            <div style="flex:1;">
                                <div class="p-name">${p.name}</div>
                                <div class="p-sub">
                                    <span class="playing-dot ${playingDot}"></span>
                                    ${p.is_playing ? 'Playing' : 'Bench'} • ${p.sel} Sel • ${p.ml_score} AI
                                </div>
                            </div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <div style="font-weight:800; font-size:15px; color: ${teamColor}">${p.credits}</div>
                            ${aiSuggest}
                            <div class="btn-add">${isSelected ? '−' : '+'}</div>
                        </div>
                    </div>
                `;
            });
            updateTracker();
            checkAutoSwap();
        }

        function togglePlayer(id) {
            const player = allPlayers.find(p => p.id === id);
            const index = myTeam.findIndex(t => t.id === id);

            if (index > -1) {
                myTeam.splice(index, 1); 
                creditsLeft += player.credits;
            } else {
                if (myTeam.length >= 11) return alert("❌ Max 11 players!");
                if (creditsLeft < player.credits) return alert("💰 Low credits!");
                if (!player.is_playing && lineupsAnnounced) return alert("⚠️ Player benched!");
                myTeam.push(player); 
                creditsLeft -= player.credits;
            }
            
            renderPlayers();
            updateAIInsights();
        }

        function updateTracker() {
            document.getElementById('playerCount').textContent = `${myTeam.length}/11`;
            document.getElementById('creditCount').textContent = creditsLeft.toFixed(1);
            
            const btnNext = document.getElementById('btnNext');
            btnNext.textContent = myTeam.length === 11 ? '✅ NEXT: C/VC' : 'NEXT: C/VC Selection';
            btnNext.className = myTeam.length === 11 ? 'btn-primary ready' : 'btn-primary';
        }

        function checkAutoSwap() {
            const benchedCount = myTeam.filter(p => !p.is_playing).length;
            const alertEl = document.getElementById('swapAlert');
            if (benchedCount > 0 && lineupsAnnounced) {
                alertEl.style.display = 'flex';
                alertEl.innerHTML = `<div><i class="fas fa-exclamation-triangle" style="color:var(--d11-red)"></i> 
                                    <span style="font-weight:600;">${benchedCount} benched players!</span></div>
                                    <button class="btn-swap" onclick="autoSwapAI()">AI Fix</button>`;
            } else {
                alertEl.style.display = 'none';
            }
        }

        async function autoSwapAI() {
            const benched = myTeam.filter(p => !p.is_playing);
            const playingAlternatives = allPlayers.filter(p => p.is_playing && !myTeam.some(t => t.id === p.id) && 
                                                             creditsLeft >= p.credits && p.role === benched[0]?.role);
            
            if (playingAlternatives.length > 0) {
                const swapIn = playingAlternatives[0];
                const swapOut = benched[0];
                
                const outIndex = myTeam.findIndex(t => t.id === swapOut.id);
                myTeam[outIndex] = swapIn;
                creditsLeft = creditsLeft - swapIn.credits + swapOut.credits;
                
                alert(`✅ AI Swap Complete!\\n${swapOut.name} (Bench) → ${swapIn.name} (Playing)`);
                renderPlayers();
            }
        }

        function announceLineups() {
            lineupsAnnounced = true;
            document.getElementById('matchStatus').innerHTML = 'MI vs CSK • <span style="color:var(--d11-green)">Lineups LIVE</span>';
            document.getElementById('lineupStatus').innerHTML = '✅ Official playing XI announced';
            renderPlayers();
            checkAutoSwap();
        }

        function updateAIInsights() {
            const aiPanel = document.getElementById('aiPanel');
            const aiSuggest = document.getElementById('aiSuggestions');
            
            if (myTeam.length > 0) {
                const topPlayer = myTeam.reduce((max, p) => p.ml_score > max.ml_score ? p : max);
                aiPanel.innerHTML = `
                    <div style="text-align:center; margin-bottom:10px;">
                        <div style="font-family:'Outfit'; font-weight:800; font-size:16px; color:var(--text-main);">${topPlayer.name}</div>
                        <div style="font-size:11px; color:var(--text-muted);">AI Score: <span style="color:var(--d11-green); font-weight:700;">${topPlayer.ml_score}</span></div>
                    </div>
                    <div class="dv-container" id="radarChart"></div>
                `;
                
                // Keep radar responsive for mobile
                let m = window.innerWidth < 768 ? 20 : 30;
                Plotly.newPlot('radarChart', [{
                    type: 'scatterpolar', r: topPlayer.radar, 
                    theta: ['Form','Consist.','Stats','Venue','Matchup'],
                    fill: 'toself', line: {color: '#8b5cf6'}, fillcolor: 'rgba(139,92,246,0.3)'
                }], {polar: {radialaxis: {range: [0,100]}}, showlegend: false, margin: {t: m, b: m, l: m, r: m}}, {displayModeBar: false, responsive: true});

                const suggestions = topPlayer.pair_suggest.filter(name => 
                    allPlayers.some(p => p.name === name && !myTeam.some(t => t.name === name))
                );
                if (suggestions.length > 0) {
                    aiSuggest.style.display = 'block';
                    aiSuggest.innerHTML = `
                        <div class="ai-insight-box pair-suggestion">
                            <i class="fas fa-lightbulb" style="color:var(--d11-orange)"></i>
                            <strong>AI Suggestion:</strong> Add <strong style="color:var(--d11-orange)">${suggestions[0]}</strong> 
                            with ${topPlayer.name} (+25% boost!)
                        </div>
                    `;
                } else {
                    aiSuggest.style.display = 'none';
                }
            }
        }

        function goToCVC() { if(myTeam.length !== 11) return alert('Select exactly 11 players!'); 
                             document.getElementById('screen-builder').style.transform = 'translateX(-100%)';
                             document.getElementById('screen-cvc').style.transform = 'translateX(0)'; renderCVC(); }
        
        function goToBuilder() { 
            document.getElementById('screen-builder').style.transform = 'translateX(0)';
            document.getElementById('screen-cvc').style.transform = 'translateX(100%)'; 
        }

        function renderCVC() {
            const list = document.getElementById('cvcListArea');
            list.innerHTML = '';
            myTeam.sort((a,b) => b.ml_score - a.ml_score).forEach(p => {
                list.innerHTML += `
                    <div class="cvc-row" onclick="showPlayerDetail(${p.id})">
                        <div>
                            <div style="font-weight:700; font-size:14px;">${p.name} (${p.role})</div>
                            <div style="font-size:11px; color:var(--text-muted);">${p.points}pts | ${p.sel}</div>
                        </div>
                        <div style="display:flex; gap:6px;">
                            <div class="circle-btn ${selectedC === p.id ? 'c-active' : ''}" onclick="selectC(${p.id});event.stopPropagation()">C</div>
                            <div class="circle-btn ${selectedVC === p.id ? 'vc-active' : ''}" onclick="selectVC(${p.id});event.stopPropagation()">VC</div>
                        </div>
                    </div>
                `;
            });
        }

        function selectC(id) { selectedC = id; renderCVC(); }
        function selectVC(id) { selectedVC = id; renderCVC(); }

        function goToPreview() {
            if(!selectedC || !selectedVC) return alert('Select C & VC first!');
            document.getElementById('screen-cvc').style.transform = 'translateX(-100%)';
            document.getElementById('screen-preview').style.transform = 'translateX(0)';
            renderPitchPreview();
        }

        function backToCVC() {
            document.getElementById('screen-preview').style.transform = 'translateX(100%)';
            document.getElementById('screen-cvc').style.transform = 'translateX(0)';
        }

        function renderPitchPreview() {
            const pitch = document.getElementById('pitchPreview');
            let total = 0;
            const roles = ['WK','BAT','AR','BOWL'];
            
            roles.forEach(role => {
                const players = myTeam.filter(p => p.role === role);
                if(players.length) {
                    let row = `<div class="pitch-role-row">`;
                    players.forEach(p => {
                        let multiplier = 1;
                        let badge = '';
                        if(p.id === selectedC) { multiplier = 2; badge = '<div class="badge-c">C</div>'; }
                        if(p.id === selectedVC) { multiplier = 1.5; badge = '<div class="badge-c" style="background:#059669;color:white;">VC</div>'; }
                        
                        const projPts = (p.points * multiplier).toFixed(0);
                        total += parseInt(projPts);
                        
                        row += `
                            <div class="pitch-player">
                                ${badge}
                                <img src="https://ui-avatars.com/api/?name=${p.name}&size=128&background=${p.team==='MI'?'2563eb':'eab308'}&color=fff" alt="${p.name}">
                                <div class="p-name">${p.name.split(' ')[0]}</div>
                                <div class="pts">${projPts}</div>
                            </div>
                        `;
                    });
                    row += `</div>`;
                    pitch.innerHTML += row;
                }
            });
            document.getElementById('totalPoints').textContent = total;
        }

        function showPlayerDetail(id) {
            const player = myTeam.find(p => p.id === id);
            if(player) updateAIInsights();
        }
    </script>
</body>
</html>
"""

# HTML render using a fixed height for Streamlit.
# 1000px ensures mobile vertical stacking has room, while desktop stays locked at 720px by the internal CSS.
components.html(html_code, height=1000, scrolling=True)
