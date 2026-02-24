import streamlit as st
import sqlite3
import pandas as pd
from streamlit_keyup import st_keyup # Ye keyboard track karega

# Database setup
conn = sqlite3.connect("vocab.db", check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS words (word TEXT, meaning TEXT)')
conn.commit()

st.set_page_config(page_title="Vocab Beast Pro", layout="centered")

# CSS for a beautiful 3D Flip Card
st.markdown("""
<style>
    .card-container { perspective: 1000px; width: 100%; height: 300px; margin: 20px auto; }
    .card-inner { position: relative; width: 100%; height: 100%; transition: transform 0.6s; transform-style: preserve-3d; cursor: pointer; }
    .card-flip { transform: rotateY(180deg); }
    .card-front, .card-back { position: absolute; width: 100%; height: 100%; backface-visibility: hidden; display: flex; align-items: center; justify-content: center; border-radius: 20px; font-size: 32px; font-weight: bold; box-shadow: 0 10px 30px rgba(0,0,0,0.2); text-align: center; padding: 20px; }
    .card-front { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
    .card-back { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; transform: rotateY(180deg); }
</style>
""", unsafe_allow_html=True)

st.title("Vocab Beast: Keyboard Edition ⚡")
st.write("Tip: Press **Space** to flip, **Enter** for next word!")

# Session state for tracking
if 'idx' not in st.session_state: st.session_state.idx = 0
if 'flipped' not in st.session_state: st.session_state.flipped = False

# Hidden Input for Keyboard Tracking
key = st_keyup("Keyboard Shortcut", key="control_input", label_visibility="collapsed")

# Simple Keyboard Logic
if key == " ": # Spacebar
    st.session_state.flipped = not st.session_state.flipped
elif key == "Enter": # Enter key
    st.session_state.idx += 1
    st.session_state.flipped = False

# Fetch Data
df = pd.read_sql_query("SELECT * FROM words", conn)

if not df.empty:
    current_word = df.iloc[st.session_state.idx % len(df)]
    flip_class = "card-flip" if st.session_state.flipped else ""
    
    # Render Card
    st.markdown(f"""
    <div class="card-container">
        <div class="card-inner {flip_class}">
            <div class="card-front">{current_word['word']}</div>
            <div class="card-back">{current_word['meaning']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning("Bhai, pehle 'Add' tab mein jaakar kuch words daalo!")

# Buttons as fallback
col1, col2 = st.columns(2)
with col1:
    if st.button("Flip (Space)"):
        st.session_state.flipped = not st.session_state.flipped
        st.rerun()
with col2:
    if st.button("Next (Enter)"):
        st.session_state.idx += 1
        st.session_state.flipped = False
        st.rerun()
