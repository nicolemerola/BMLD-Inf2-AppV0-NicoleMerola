import streamlit as st
import pandas as pd
from functions.kalorienrechner import BMR_rechnen

st.title("Kalorienbedarf Rechner")
st.write("Berechne deinen täglichen Kalorienbedarf.")

# Session State initialisieren
for key in ("geschlecht", "gewicht", "groesse", "alter", "aktivitaet", "kalorien"):
    if key not in st.session_state:
        st.session_state[key] = None

# Falls data_df noch nicht existiert
if "data_df" not in st.session_state:
    st.session_state["data_df"] = pd.DataFrame(
        columns=["timestamp", "geschlecht", "gewicht", "groesse", "alter", "aktivitaet", "kalorien"]
    )

with st.form("calorie_form"):
    geschlecht = st.selectbox("Geschlecht", ["Mann", "Frau"], key="geschlecht")
    gewicht = st.number_input("Gewicht (kg)", min_value=30, max_value=200, key="gewicht")
    groesse = st.number_input("Größe (cm)", min_value=120, max_value=220, key="groesse")
    alter = st.number_input("Alter", min_value=10, max_value=100, key="alter")

    aktivitaet = st.selectbox(
        "Aktivitätslevel",
        ["wenig Bewegung", "leicht aktiv", "moderat aktiv", "sehr aktiv"],
        key="aktivitaet"
    )

    submit = st.form_submit_button("Berechnen")

if submit:
    if geschlecht == "Mann":
        bmr = BMR_rechnen(gewicht, groesse, alter, geschlecht)
    else:
        bmr = BMR_rechnen(gewicht, groesse, alter, "Frau")

    faktor = {
        "wenig Bewegung": 1.2,
        "leicht aktiv": 1.375,
        "moderat aktiv": 1.55,
        "sehr aktiv": 1.725
    }

    kalorien = bmr * faktor[aktivitaet]
    st.session_state["kalorien"] = kalorien

    new_row = {
        "timestamp": pd.Timestamp.now(),
        "geschlecht": geschlecht,
        "gewicht": gewicht,
        "groesse": groesse,
        "alter": alter,
        "aktivitaet": aktivitaet,
        "kalorien": kalorien
    }

    st.session_state["data_df"] = pd.concat(
        [st.session_state["data_df"], pd.DataFrame([new_row])],
        ignore_index=True
    )

    data_manager = st.session_state["data_manager"]
    data_manager.save_user_data(st.session_state["data_df"], "data.csv")

# Ergebnis anzeigen
if st.session_state["kalorien"] is not None:
    st.metric("Dein täglicher Kalorienbedarf", f"{st.session_state['kalorien']:.0f} kcal")

# Eingaben anzeigen
st.write("### Eingaben")
st.write({
    "Geschlecht": st.session_state["geschlecht"],
    "Gewicht": st.session_state["gewicht"],
    "Größe": st.session_state["groesse"],
    "Alter": st.session_state["alter"],
    "Aktivität": st.session_state["aktivitaet"],
})

# Verlauf anzeigen
if not st.session_state["data_df"].empty:
    st.write("### Verlauf")
    st.dataframe(st.session_state["data_df"])

  