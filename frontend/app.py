import streamlit as st
import sys
import os
from dotenv import load_dotenv
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import requests

load_dotenv()


API_URL = os.getenv("API_URL")

if "sub_msg" not in st.session_state:
    st.session_state.sub_msg = None
if "sub_type" not in st.session_state:
    st.session_state.sub_type = None
if "unsub_msg" not in st.session_state:
    st.session_state.unsub_msg = None
if "unsub_type" not in st.session_state:
    st.session_state.unsub_type = None




st.set_page_config(
    page_title="Fabrizio Romano Lite",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

POPULAR_TEAMS = [
    "Manchester City", "Manchester United", "Arsenal", "Liverpool",
    "Chelsea", "Tottenham", "Real Madrid", "Barcelona", "Bayern Munich",
    "PSG", "Juventus", "AC Milan", "Inter Milan", "Borussia Dortmund",
    "Atletico Madrid", "Ajax", "Napoli", "Roma"
]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bitcount+Grid+Double:wght@100..900&family=Kumar+One&family=Playwrite+GB+J:ital,wght@0,100..400;1,100..400&family=Urbanist:ital,wght@0,100..900;1,100..900&family=Cormorant+Garamond:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

html, body { overflow-x: hidden; }

[data-testid="stAppViewContainer"] {
    min-height: 100vh;
    background:
        radial-gradient(ellipse 90% 55% at 50% -5%, rgba(109,40,217,0.28) 0%, transparent 65%),
        radial-gradient(ellipse 55% 45% at 85% 75%, rgba(37,99,235,0.13) 0%, transparent 60%),
        radial-gradient(ellipse 45% 40% at 10% 85%, rgba(109,40,217,0.09) 0%, transparent 55%),
        #06060e;
    font-family: 'Inter', sans-serif;
    color: #f0f0f0;
}

[data-testid="stHeader"] { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }

.block-container {
    max-width: 720px !important;
    margin: 0 auto !important;
    padding: 0 2rem 5rem !important;
}
            
.app-logo{
    font-family: "Playwrite GB J", cursive;
    font-size: 2.8rem;
    font-weight: 400;
    color: #ffffff;
    text-align: center;
    margin-top: 20px;
    margin-bottom: 50px;
    line-height: 1.1;
}           

/* ── NAV ── */
.frl-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 32px 0 0;
    margin-bottom: 0;
}
.frl-nav-brand {
    font-family: 'Inter', sans-serif;
    font-size: .78rem;
    font-weight: 600;
    letter-spacing: 3.5px;
    text-transform: uppercase;
    color: rgba(255,255,255,.85);
}
.frl-nav-pill {
    font-size: .65rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(255,255,255,.28);
    border: 1px solid rgba(255,255,255,.09);
    padding: 5px 13px;
    border-radius: 999px;
}

/* ── HERO ── */
.frl-hero {
    padding: 20px 0 40px;
    text-align: center;
}
.frl-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(139,92,246,.1);
    border: 1px solid rgba(139,92,246,.22);
    border-radius: 999px;
    padding: 5px 15px;
    font-size: .68rem;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #b197fc;
    margin-bottom: 36px;
}
.frl-badge-dot {
    width: 5px; height: 5px;
    background: #b197fc;
    border-radius: 50%;
    animation: blink 2s ease-in-out infinite;
}
@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: .25; }
}
.frl-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(2.5rem, 7vw, 4.5rem);
    font-weight: 700;
    line-height: .98;
    letter-spacing: -.5px;
    color: #ffffff;
    margin-bottom: 28px;
    text-align:center        
}
.frl-title-accent {
    background: linear-gradient(130deg, #a78bfa 0%, #818cf8 60%, #60a5fa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.frl-sub {
    font-size: .98rem;
    color: rgba(255,255,255,.32);
    line-height: 1.7;
    font-weight: 300;
    max-width: 460px;
    text-align: center;
    margin: 0 auto;
}

/* ── STATS ── */
.frl-stats {
    display: flex;
    gap: 0;
    margin: 40px 0 48px;
    border-top: 1px solid rgba(255,255,255,.06);
    border-bottom: 1px solid rgba(255,255,255,.06);
    padding: 24px 0;
}
.frl-stat {
    flex: 1;
    border-right: 1px solid rgba(255,255,255,.06);
    padding: 0 16px;
    text-align: center;
}
.frl-stat:first-child { padding-left: 0; }
.frl-stat:last-child { border-right: none; }
.frl-stat-val {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #ffffff;
    line-height: 1;
}
.frl-stat-label {
    font-size: .65rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(255,255,255,.22);
    margin-top: 7px;
}

/* ── CLEAN INPUT ALIGNMENT ── */
div[data-testid="stTextInput"] label,
div[data-testid="stSelectbox"] label {
    text-align: center !important;
    width: 100% !important;
    color: rgba(255, 255, 255, 0.45) !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 1.2px !important;
    text-transform: uppercase !important;
    margin-bottom: 8px !important;
}

div[data-testid="stTextInput"] input, 
div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    text-align: left !important;        
}

div[data-testid="stTextInput"],
div[data-testid="stSelectbox"] {
    margin-bottom: 24px !important;
}

/* ── BUTTON STYLING & POSITIONING ── */
div[data-testid="stButton"] {
    display: block !important;       
    text-align: center !important;   
    width: 100% !important;
    margin-top: 15px !important;
    margin-bottom: 25px !important;
}

div[data-testid="stButton"] button {
    display: inline-block !important;       
    margin: 0 auto !important;       
    width: 280px !important;            
    height: 60px !important;
    border-radius: 18px !important;
    background: linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%) !important;
    color: rgba(255,255,255,.95) !important;
    border: none !important;
    font-size: .88rem !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: .8px !important;
    text-transform: uppercase !important;
    transition: all .2s ease !important;
    cursor: pointer !important;
}

div[data-testid="stButton"] button:hover {
    background: linear-gradient(135deg, #6d28d9 0%, #4c1d95 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 14px 40px rgba(124,58,237,.3) !important;
}

div[data-testid="stButton"] button:active {
    transform: translateY(0px) !important;
}

/* ── ALERTS ── */
.frl-alert {
    padding: 15px 18px;
    border-radius: 13px;
    font-size: .85rem;
    line-height: 1.65;
    margin-top: 12px;
}
.frl-success {
    background: rgba(139,92,246,.07);
    border: 1px solid rgba(139,92,246,.18);
    color: #c4b5fd;
}
.frl-error {
    background: rgba(239,68,68,.06);
    border: 1px solid rgba(239,68,68,.16);
    color: #fca5a5;
}

/* ── FOOTER ── */
.frl-footer {
    text-align: center;
    padding: 48px 0 24px;
    border-top: 1px solid rgba(255,255,255,.05);
    margin-top: 48px;
}
.frl-footer-text {
    font-size: .75rem;
    color: rgba(255,255,255,.18);
    letter-spacing: .5px;
    margin-bottom: 16px;
}
.frl-chips {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 8px;
}
.frl-chip {
    background: rgba(255,255,255,.03);
    border: 1px solid rgba(255,255,255,.06);
    border-radius: 999px;
    padding: 4px 12px;
    font-size: .68rem;
    color: rgba(255,255,255,.2);
    letter-spacing: .5px;
}

/* ── GLOBAL MOBILE RESPONSIVENESS (CRITICAL) ── */
@media (max-width: 640px) {
    .block-container { 
        padding: 0 1.25rem 3rem !important; 
    }
    .app-logo {
        font-size: 2.2rem;
        margin-bottom: 30px;
    }
    .frl-hero { 
        padding: 20px 0 30px; 
    }
    .frl-title { 
        font-size: 2.8rem !important; 
    }
    .frl-sub {
        font-size: 0.9rem;
    }
    .frl-stats { 
        flex-wrap: wrap; 
        gap: 12px; 
        padding: 16px 0;
        margin: 30px 0 40px;
    }
    .frl-stat { 
        flex: 1 1 calc(50% - 12px); 
        border-right: none; 
        padding: 4px; 
    }
    .frl-stat:nth-child(odd) {
        border-right: 1px solid rgba(255,255,255,.06);
    }
    div[data-testid="stButton"] button {
        width: 100% !important; /* Button takes comfortable width on narrow devices */
        max-width: 320px;
    }
    /* Forces Streamlit column wrappers to scale gracefully on mobiles */
    div[data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
    }
}

.subscribe-title,
.unsubscribe-title{
    text-align:center !important;
}
</style>
""", unsafe_allow_html=True)

# NAV
st.markdown("""
<div class="app-logo">
    farzi romano
</div>
""", unsafe_allow_html=True)

# HERO
st.markdown("""
<div class="frl-hero">
    <div class="frl-title">
        Your club.<br>
        <span class="frl-title-accent">Every transfer.</span><br>
        Every morning.
    </div>
    <div class="frl-sub">
        AI-powered briefings sourced from Fabrizio Romano,
        David Ornstein and Tier-1 journalists —
        delivered to your inbox at 9 AM daily.
    </div>
</div>
<div class="frl-stats">
    <div class="frl-stat">
        <div class="frl-stat-val">9 AM</div>
        <div class="frl-stat-label">Daily</div>
    </div>
    <div class="frl-stat">
        <div class="frl-stat-val">Tier 1</div>
        <div class="frl-stat-label">Sources</div>
    </div>
    <div class="frl-stat">
        <div class="frl-stat-val">18+</div>
        <div class="frl-stat-label">Clubs</div>
    </div>
    <div class="frl-stat">
        <div class="frl-stat-val">Free</div>
        <div class="frl-stat-label">Always</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── SUBSCRIBE SECTION ──
st.markdown("""
<div class="frl-title subscribe-title" style="font-size:2.3rem;margin-bottom:12px;text-align:center;">Subscribe</div>
""", unsafe_allow_html=True)

team = st.selectbox("Your Club", POPULAR_TEAMS)
email = st.text_input("Email Address", placeholder="yourname@example.com")

# Responsive structural columns layout
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Here We Go →"):
        if not email or "@" not in email:
            st.session_state.sub_msg = "Please enter a valid email address."
            st.session_state.sub_type = "error"
        else:
            res = requests.post(f"{API_URL}/subscribe", json={"email": email, "team": team})
            if res.status_code == 200:
                st.session_state.sub_msg = f"You're in! First {team} briefing arrives tomorrow at 9 AM."
                st.session_state.sub_type = "success"
            elif res.status_code == 409:
                st.session_state.sub_msg = "This email is already subscribed."
                st.session_state.sub_type = "error"
            else:
                st.session_state.sub_msg = "Something went wrong. Try again."
                st.session_state.sub_type = "error"

    if st.session_state.sub_msg:
        css_class = "frl-success" if st.session_state.sub_type == "success" else "frl-error"
        icon = "✓" if st.session_state.sub_type == "success" else "⚠"
        st.markdown(f'<div class="frl-alert {css_class}">{icon} &nbsp;{st.session_state.sub_msg}</div>', unsafe_allow_html=True)


# ── UNSUBSCRIBE SECTION ──
st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)
st.markdown("""
<div class="frl-title unsubscribe-title" style="font-size:2.3rem;margin-top:20px;margin-bottom:18px;text-align:center;">Unsubscribe</div>
""", unsafe_allow_html=True)

unsub_email = st.text_input("Email Address", placeholder="yourname@example.com", key="unsub")

# Responsive structural columns layout
u_col1, u_col2, u_col3 = st.columns([1, 2, 1])
with u_col2:
    if st.button("Remove Me"):
        if not unsub_email or "@" not in unsub_email:
            st.session_state.unsub_msg = "Please enter a valid email address."
            st.session_state.unsub_type = "error"
        else:
            res = requests.delete(f"{API_URL}/unsubscribe/{unsub_email}")
            if res.status_code == 200:
                st.session_state.unsub_msg = "Unsubscribed successfully."
                st.session_state.unsub_type = "success"
            elif res.status_code == 404:
                st.session_state.unsub_msg = "Email not found."
                st.session_state.unsub_type = "error"
            else:
                st.session_state.unsub_msg = "Something went wrong. Try again."
                st.session_state.unsub_type = "error"

    if st.session_state.unsub_msg:
        css_class = "frl-success" if st.session_state.unsub_type == "success" else "frl-error"
        icon = "✓" if st.session_state.unsub_type == "success" else "⚠"
        st.markdown(f'<div class="frl-alert {css_class}">{icon} &nbsp;{st.session_state.unsub_msg}</div>', unsafe_allow_html=True)

# ── FOOTER ──
st.markdown("""
<div class="frl-footer">
    <div class="frl-footer-text">© 2026 Fabrizio Romano Lite · Transfer Intelligence · Daily at 9 AM</div>
    <div class="frl-chips">
        <span class="frl-chip">LangGraph</span>
        <span class="frl-chip">Groq · Llama 3</span>
        <span class="frl-chip">Tavily</span>
        <span class="frl-chip">Supabase</span>
    </div>
</div>
""", unsafe_allow_html=True)