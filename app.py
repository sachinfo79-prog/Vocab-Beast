import streamlit as st
import sqlite3
import pandas as pd
import PyPDF2
import re

# Database connection
conn = sqlite3.connect("vocab.db", check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS words (word TEXT, meaning TEXT)')
conn.commit()

st.set_page_config(page_title="Vocab Beast Pro", layout="wide")

# Sidebar for PDF Upload
with st.sidebar:
    st.title("📤 PDF se Words Nikalo")
    pdf_file = st.file_uploader("Apni PDF select karo", type="pdf")
    
    if pdf_file:
        if st.button("Extract aur Save Karein"):
            reader = PyPDF2.PdfReader(pdf_file)
            count = 0
            for page in reader.pages:
                text = page.extract_text()
                # Ye pattern "Word - Meaning" ya "Word: Meaning" ko dhoondta hai
                matches = re.findall(r'([A-Za-z]+)\s*[:\-]\s*(.+)', text)
                for word, meaning in matches:
                    c.execute("INSERT INTO words (word, meaning) VALUES (?, ?)", (word.strip(), meaning.strip()))
                    count += 1
            conn.commit()
            st.success(f"Bhai, {count} naye words add ho gaye! 🎉")
            st.rerun()

# --- Main Interface (Cards) ---
st.title("Vocab Beast: PDF Edition ⚡")

if 'idx' not in st.session_state: st.session_state.idx = 0
if 'flipped' not in st.session_state: st.session_state.flipped = False

df = pd.read_sql_query("SELECT * FROM words", conn)

if not df.empty:
    # Card Display Logic (Wahi purana mast wala)
    current_word = df.iloc[st.session_state.idx % len(df)]
    # ... (Flip Card CSS aur HTML yahan aayega)
    st.info(f"Abhi total {len(df)} words hain tere paas.")
else:
    st.warning("Bhai, sidebar se PDF upload karo ya manually add karo!")

# Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Flip (Palto)"):
        st.session_state.flipped = not st.session_state.flipped
        st.rerun()
with col2:
    if st.button("Next (Agla)"):
        st.session_state.idx += 1
        st.session_state.flipped = False
        st.rerun()
