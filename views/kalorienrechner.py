import streamlit as st
from functions.kalorienrechner import BMR_rechner
from utils.data_manager import DataManager

st.title("Kalorienbedarf Rechner")
st.write("Berechne deinen täglichen Kalorienbedarf.")

# initialize session state entries if they don't exist yet
for key in ("geschlecht", "gewicht", "groesse", "alter", "aktivitaet", "kalorien"):
    if key not in st.session_state:
        st.session_state[key] = None

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
    # compute BMR
    if geschlecht == "Mann":
        bmr = BMR_rechner(gewicht, groesse, alter, geschlecht)
    else:
        bmr = BMR_rechner(gewicht, groesse, alter, "Frau")

    faktor = {
        "wenig Bewegung": 1.2,
        "leicht aktiv": 1.375,
        "moderat aktiv": 1.55,
        "sehr aktiv": 1.725
    }

    kalorien = bmr * faktor[aktivitaet]
    st.session_state.kalorien = kalorien

# show stored result if any
if st.session_state.kalorien is not None:
    st.metric("Dein täglicher Kalorienbedarf", f"{st.session_state.kalorien:.0f} kcal")

# example of using session_state to retain inputs between page reloads
st.write("### Eingaben (Session State)")
st.write({
    "Geschlecht": st.session_state.geschlecht,
    "Gewicht": st.session_state.gewicht,
    "Größe": st.session_state.groesse,
    "Alter": st.session_state.alter,
    "Aktivität": st.session_state.aktivitaet,
})
    data_manager = DataManager()
    data_manager.save_user_data(st.session_state['data_df'], 'data.csv')
