
import streamlit as st
import random
import time
from statistics import mean

# -----------------------------
# Einstellungen
# -----------------------------
ANZAHL_WOERTER = 50

farben = {
    "Rot": "red",
    "Gelb": "gold",
    "Blau": "blue",
    "Grün": "green"
}

# -----------------------------
# Session State initialisieren
# -----------------------------
if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.index = 0
    st.session_state.stimuli = []
    st.session_state.daten = []
    st.session_state.startzeit = 0
    st.session_state.finished = False

# -----------------------------
# Stimuli erzeugen
# -----------------------------
def generate_stimuli():
    woerter = list(farben.keys())
    stimuli = []

    for _ in range(ANZAHL_WOERTER):
        wort = random.choice(woerter)
        farbname = random.choice(woerter)

        typ = "Gleich" if wort == farbname else "Konflikt"

        stimuli.append({
            "wort": wort,
            "farbe": farben[farbname],
            "richtige_antwort": farbname,
            "typ": typ
        })

    return stimuli


# -----------------------------
# Startscreen
# -----------------------------
st.title("🧠 Stroop-Test")

if not st.session_state.started:
    st.write("""
### Anleitung
- Du siehst ein Wort in einer bestimmten FARBE
- Du musst die **FARBE** drücken, nicht das Wort lesen

### Tasten (hier Buttons):
- Rot = 1  
- Gelb = 2  
- Blau = 0  
- Grün = 9  

👉 Klicke Start, um zu beginnen
""")

    if st.button("Start"):
        st.session_state.started = True
        st.session_state.stimuli = generate_stimuli()
        st.rerun()

# -----------------------------
# Test läuft
# -----------------------------
elif not st.session_state.finished:

    stimulus = st.session_state.stimuli[st.session_state.index]

    st.write(f"Wort {st.session_state.index + 1} / {ANZAHL_WOERTER}")

    st.markdown(
        f"<h1 style='color:{stimulus['farbe']}; text-align:center;'>"
        f"{stimulus['wort']}</h1>",
        unsafe_allow_html=True
    )

    # Startzeit setzen beim ersten Laden
    if st.session_state.startzeit == 0:
        st.session_state.startzeit = time.time()

    col1, col2, col3, col4 = st.columns(4)

    def antwort(antwort_text):
        rt = time.time() - st.session_state.startzeit
        stim = st.session_state.stimuli[st.session_state.index]

        richtig = (antwort_text == stim["richtige_antwort"])

        st.session_state.daten.append({
            "typ": stim["typ"],
            "richtig": richtig,
            "reaktionszeit": rt
        })

        st.session_state.index += 1
        st.session_state.startzeit = time.time()

        if st.session_state.index >= ANZAHL_WOERTER:
            st.session_state.finished = True

        st.rerun()

    with col1:
        if st.button("Rot (1)"):
            antwort("Rot")

    with col2:
        if st.button("Gelb (2)"):
            antwort("Gelb")

    with col3:
        if st.button("Blau (0)"):
            antwort("Blau")

    with col4:
        if st.button("Grün (9)"):
            antwort("Grün")

# -----------------------------
# Auswertung
# -----------------------------
else:

    daten = st.session_state.daten

    fehler = len([d for d in daten if not d["richtig"]])
    genauigkeit = ((ANZAHL_WOERTER - fehler) / ANZAHL_WOERTER) * 100

    gleich = [d for d in daten if d["typ"] == "Gleich"]
    konflikt = [d for d in daten if d["typ"] == "Konflikt"]

    gleich_rt = mean([d["reaktionszeit"] for d in gleich]) if gleich else 0
    konflikt_rt = mean([d["reaktionszeit"] for d in konflikt]) if konflikt else 0

    stroop_effekt = konflikt_rt - gleich_rt

    st.title("📊 Ergebnis")

    st.write(f"Fehler gesamt: {fehler}")
    st.write(f"Genauigkeit: {genauigkeit:.1f}%")
    st.write(f"Ø Reaktionszeit: {mean([d['reaktionszeit'] for d in daten]):.3f} s")

    st.subheader("Gleich-Bedingung")
    st.write(f"Ø RT: {gleich_rt:.3f} s")

    st.subheader("Konflikt-Bedingung")
    st.write(f"Ø RT: {konflikt_rt:.3f} s")

    st.subheader("Stroop-Effekt")
    st.write(f"{stroop_effekt:.3f} Sekunden")