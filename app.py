import streamlit as st
import sqlite3
import pandas as pd

# Database Setup
def init_db():
    conn = sqlite3.connect("vocab_beast.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS flashcards
                 (id INTEGER PRIMARY KEY, word TEXT UNIQUE, meaning TEXT, level INTEGER)''')
    conn.commit()
    conn.close()

init_db()

# Simple 3D Flip CSS
st.markdown("""
<style>
    .flip-card { width: 300px; height: 200px; perspective: 1000px; margin: auto; }
    .flip-card-inner { position: relative; width: 100%; height: 100%; transition: transform 0.6s; transform-style: preserve-3d; cursor: pointer; }
    .flip-card:hover .flip-card-inner { transform: rotateY(180deg); }
    .front, .back { position: absolute; width: 100%; height: 100%; backface-visibility: hidden; display: flex; align-items: center; justify-content: center; border-radius: 15px; font-size: 24px; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
    .front { background: white; color: black; }
    .back { background: #2e7d32; color: white; transform: rotateY(180deg); }
</style>
""", unsafe_allow_html=True)

st.title("Vocab Beast v0.1 (Base)")

tab1, tab2 = st.tabs(["Practice", "Add New"])

with tab2:
    word = st.text_input("English Word")
    meaning = st.text_input("Hindi Meaning")
    if st.button("Save"):
        conn = sqlite3.connect("vocab_beast.db")
        try:
            conn.execute("INSERT INTO flashcards (word, meaning, level) VALUES (?, ?, 0)", (word, meaning))
            conn.commit()
            st.success("Saved! [cite: 2026-02-22]")
        except: st.error("Already exists! [cite: 2026-02-22]")
        conn.close()

with tab1:
    conn = sqlite3.connect("vocab_beast.db")
    df = pd.read_sql_query("SELECT * FROM flashcards", conn)
    conn.close()
    if not df.empty:
        card = df.iloc[0]
        st.markdown(f'<div class="flip-card"><div class="flip-card-inner"><div class="front">{card["word"]}</div><div class="back">{card["meaning"]}</div></div></div>', unsafe_allow_html=True)
    else: st.write("No words yet.")