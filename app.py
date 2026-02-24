import streamlit as st
import sqlite3
import pandas as pd
import PyPDF2
import re

# --- DATABASE SETUP ---
conn = sqlite3.connect("vocab.db", check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS words (word TEXT, meaning TEXT)')
conn.commit()

# --- PAGE CONFIG ---
st.set_page_config(page_title="Vocab Beast Pro", layout="centered")

# --- CSS (Purani Styling + New Look) ---
st.markdown("""
<style>
    .card-container { perspective: 1000px; width: 100%; height: 300px; margin: 20px auto; }
    .card-inner { position: relative; width: 100%; height: 100%; transition: transform 0.6s; transform-style: preserve-3d; cursor: pointer; }
    .card-flip { transform: rotateY(180deg); }
    .card-front, .card-back { position: absolute; width: 100%; height: 100%; backface-visibility: hidden; display: flex; align-items: center; justify-content: center; border-radius: 20px; font-size: 32px; font-weight: bold; color: white; text-align: center; padding: 20px; }
    .card-front { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border: 3px solid #fff; }
    .card-back { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); transform: rotateY(180deg); border: 3px solid #fff; }
    .stButton>button { width: 100%; border-radius: 10px; height: 50px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: PDF EXTRACTION ---
with st.sidebar:
    st.header("📤 Bulk Upload (PDF)")
    uploaded_file = st.file_uploader("Vocab PDF select karo", type="pdf")
    
    if uploaded_file:
        if st.button("Extract Words"):
            reader = PyPDF2.PdfReader(uploaded_file)
            count = 0
            for page in reader.pages:
                text = page.extract_text()
                # Pattern for English Word - Hindi/Eng Meaning
                matches = re.findall(r'([A-Za-z]+)\s*[:\-–]\s*(.+)', text)
                for word, meaning in matches:
                    c.execute("INSERT INTO words (word, meaning) VALUES (?, ?)", (word.strip(), meaning.strip()))
                    count += 1
            conn.commit()
            st.success(f"Bhai, {count} words database mein save ho gaye! 🎉")
            st.rerun()
    
    if st.button("Clear Database (Reset)"):
        c.execute("DELETE FROM words")
        conn.commit()
        st.warning("Saara data uda diya!")
        st.rerun()

# --- MAIN APP LOGIC ---
st.title("Vocab Beast Pro ⚡")

if 'idx' not in st.session_state: st.session_state.idx = 0
if 'flipped' not in st.session_state: st.session_state.flipped = False

# Fetching Data
df = pd.read_sql_query("SELECT * FROM words", conn)

if not df.empty:
    current_word = df.iloc[st.session_state.idx % len(df)]
    flip_class = "card-flip" if st.session_state.flipped else ""
    
    # Flip Card UI
    st.markdown(f'''
    <div class="card-container">
        <div class="card-inner {flip_class}">
            <div class="card-front">{current_word['word']}</div>
            <div class="card-back">{current_word['meaning']}</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.write(f"📊 Progress: Word {st.session_state.idx + 1} of {len(df)}")

    # Control Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Flip (Palto)"):
            st.session_state.flipped = not st.session_state.flipped
            st.rerun()
    with col2:
        if st.button("➡️ Next (Agla)"):
            st.session_state.idx += 1
            st.session_state.flipped = False
            st.rerun()
else:
    st.info("Bhai, abhi database khali hai. Sidebar se PDF upload kar ya words dalo!")

# Add Word Manually
with st.expander("➕ Ek-ek karke word jodo"):
    new_w = st.text_input("English Word")
    new_m = st.text_input("Hindi Meaning")
    if st.button("Save Word"):
        if new_w and new_m:
            c.execute("INSERT INTO words (word, meaning) VALUES (?, ?)", (new_w, new_m))
            conn.commit()
            st.success("Save ho gaya!")
            st.rerun()
