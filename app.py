import streamlit as st
import requests
from bs4 import BeautifulSoup
from collections import Counter
import random

st.set_page_config(page_title="Togel Predictor", layout="wide")
st.title("🎯 Togel Predictor Web")

# -----------------------------
# INPUT USER
# -----------------------------
url = st.text_input("Masukkan link website result (copy-paste):")
selector = st.text_input("Masukkan selector HTML angka (default '.result')", ".result")
mode = st.selectbox("Pilih mode:", [2,3,4,5])

# -----------------------------
# FUNCTIONS
# -----------------------------
def get_history(url, selector):
    """Scrape result dari website"""
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        results = [item.text.strip() for item in soup.select(selector)]
        return results
    except Exception as e:
        st.error(f"Gagal ambil data: {e}")
        return []

def analyze_frequency(history):
    """Hitung frekuensi tiap angka"""
    all_digits = "".join(history)
    freq = Counter(all_digits)
    return freq

def analyze_delay(history):
    """Hitung delay tiap angka"""
    last_pos = {}
    delay_count = {}
    for i, result in enumerate(history[::-1]):  # mulai dari result terbaru
        for d in result:
            if d not in last_pos:
                last_pos[d] = i
                delay_count[d] = i + 1
    return delay_count

def generate_candidates(freq, digits, count=20):
    """Generate kandidat angka berdasarkan frekuensi"""
    digits_list = list(freq.keys())
    weights = list(freq.values())
    candidates = []
    for _ in range(count):
        num = "".join(random.choices(digits_list, weights, k=digits))
        candidates.append(num)
    return candidates

# -----------------------------
# PROSES
# -----------------------------
if st.button("Generate Kandidat"):
    if not url:
        st.warning("Masukkan link website terlebih dahulu.")
    else:
        history = get_history(url, selector)
        if not history:
            st.error("Gagal membaca history. Cek URL & selector.")
        else:
            st.success(f"History terbaca: {len(history)} periode")
            freq = analyze_frequency(history)
            delay = analyze_delay(history)
            candidates = generate_candidates(freq, digits=mode, count=20)

            # -----------------------------
            # TAMPILAN USER-FRIENDLY
            # -----------------------------
            st.subheader("📊 Statistik Angka")
            st.write("**Angka paling sering muncul:**")
            freq_str = " | ".join([f"{k}: {v}x" for k,v in sorted(freq.items(), key=lambda x:x[1], reverse=True)])
            st.text(freq_str)

            st.write("**Angka lama tidak muncul:**")
            delay_str = " | ".join([f"{k}: {v} periode" for k,v in sorted(delay.items(), key=lambda x:x[1], reverse=True)])
            st.text(delay_str)

            st.subheader(f"🎯 Top {len(candidates)} Kandidat {mode}D")
            for idx, c in enumerate(candidates, start=1):
                st.text(f"{idx}. {c}")

            st.info("Selesai! Pilih angka dari kandidat di atas untuk dipasang.")
