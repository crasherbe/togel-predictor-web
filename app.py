import streamlit as st
from collections import Counter
import random

# -----------------------------
# SETUP HALAMAN
# -----------------------------
st.set_page_config(page_title="Togel Predictor", layout="wide")
st.title("🎯 Togel Predictor Web (Copy-Paste Fixed Version)")

# -----------------------------
# INPUT USER
# -----------------------------
history_input = st.text_area(
    "Paste semua result history (satu angka per line atau semua angka digabung):"
)
mode = st.selectbox("Pilih mode:", [2,3,4,5])

# -----------------------------
# FUNCTIONS
# -----------------------------
def parse_history(history_input):
    """Ubah input user jadi list result, buang kosong/non-angka"""
    lines = history_input.splitlines()
    results = [line.strip() for line in lines if line.strip() and any(c.isdigit() for c in line.strip())]
    return results

def analyze_frequency(history):
    """Hitung frekuensi tiap angka"""
    all_digits = "".join(history)
    freq = Counter([c for c in all_digits if c.isdigit()])
    return freq

def analyze_delay(history):
    """Hitung delay tiap angka"""
    last_pos = {}
    delay_count = {}
    for i, result in enumerate(history[::-1]):
        for d in result:
            if d.isdigit() and d not in last_pos:
                last_pos[d] = i
                delay_count[d] = i + 1
    return delay_count

def generate_candidates(freq, digits, count=20):
    """Generate kandidat angka berdasarkan frekuensi, aman 100%"""
    digits_list = list(freq.keys())
    weights = list(freq.values())
    candidates = []

    if not digits_list:
        return ["Tidak ada angka valid di history"] * count

    while len(candidates) < count:
        num = "".join(random.choices(digits_list, weights, k=digits))
        if len(num) == digits:
            candidates.append(num)

    return candidates

# -----------------------------
# GENERATE & TAMPIL
# -----------------------------
if st.button("Generate Kandidat"):
    history = parse_history(history_input)
    if not history:
        st.warning("Paste dulu result history yang valid!")
    else:
        freq = analyze_frequency(history)
        delay = analyze_delay(history)
        candidates = generate_candidates(freq, digits=mode, count=20)

        # Statistik frekuensi
        st.subheader("📊 Statistik Angka")
        st.write("**Angka paling sering muncul:**")
        st.text(" | ".join([f"{k}: {v}x" for k,v in sorted(freq.items(), key=lambda x:x[1], reverse=True)]))

        # Statistik delay
        st.write("**Angka lama tidak muncul:**")
        st.text(" | ".join([f"{k}: {v} periode" for k,v in sorted(delay.items(), key=lambda x:x[1], reverse=True)]))

        # Top kandidat angka
        st.subheader(f"🎯 Top {len(candidates)} Kandidat {mode}D")
        for idx, c in enumerate(candidates, start=1):
            st.text(f"{idx}. {c}")

        st.info("Selesai! Pilih angka dari kandidat di atas untuk dipasang.")
