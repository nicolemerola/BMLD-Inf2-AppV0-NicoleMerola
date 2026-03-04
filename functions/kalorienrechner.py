import streamlit as st

st.title("Kalorienbedarf Rechner")

st.write("Berechne deinen täglichen Kalorienbedarf.")

with st.form("calorie_form"):
    geschlecht = st.selectbox("Geschlecht", ["Mann", "Frau"])
    gewicht = st.number_input("Gewicht (kg)", min_value=30, max_value=200)
    groesse = st.number_input("Größe (cm)", min_value=120, max_value=220)
    alter = st.number_input("Alter", min_value=10, max_value=100)

    aktivitaet = st.selectbox(
        "Aktivitätslevel",
        ["wenig Bewegung", "leicht aktiv", "moderat aktiv", "sehr aktiv"]
    )

    submit = st.form_submit_button("Berechnen")

if submit:
    if geschlecht == "Mann":
        bmr = 10 * gewicht + 6.25 * groesse - 5 * alter + 5
    else:
        bmr = 10 * gewicht + 6.25 * groesse - 5 * alter - 161

    faktor = {
        "wenig Bewegung": 1.2,
        "leicht aktiv": 1.375,
        "moderat aktiv": 1.55,
        "sehr aktiv": 1.725
    }

    kalorien = bmr * faktor[aktivitaet]

    st.metric("Dein täglicher Kalorienbedarf", f"{kalorien:.0f} kcal")
    