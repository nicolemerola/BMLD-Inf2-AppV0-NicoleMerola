import streamlit as st
import pandas as pd

st.set_page_config(page_title="Meine App", page_icon=":material/home:")

from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# DataManager mit WebDAV initialisieren
data_manager = DataManager(
    fs_protocol="webdav",
    fs_root_folder="Bmld1"
)

# Für Unterseiten verfügbar machen
st.session_state["data_manager"] = data_manager

# Login / Registrierung
login_manager = LoginManager(data_manager)
login_manager.login_register()

# Nutzerspezifische Daten laden
if "data_df" not in st.session_state:
    st.session_state["data_df"] = data_manager.load_user_data(
        "data.csv",
        initial_value=pd.DataFrame(),
        parse_dates=["timestamp"]
    )

pg_home = st.Page("views/home.py", title="Home", icon=":material/home:", default=True)
pg_kalorien = st.Page("views/kalorienrechner.py", title="Kalorienrechner", icon=":material/info:")

pg = st.navigation([pg_home, pg_kalorien])
pg.run()

