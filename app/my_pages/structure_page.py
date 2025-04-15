import streamlit as st
from utils.helpers import AIRBNB_COLORS

def show(logo_base64):
    st.header("📂 Programmstruktur")
    
    st.markdown("""
    ```plaintext
    airbnb_dashboard_app/
    └── app/
        ├── main.py                         : Einstiegspunkt
        ├── controller.py                   : AppController-Klasse
        │
        ├── pages/
        │   ├── home_page.py                : Präsentationsstartseite
        │   ├── structure_page.py           : Programmstruktur (diese Seite)
        │   ├── info_page.py                : Dateninfo & Hinweise
        │   ├── upload_page.py              : CSV-Upload & Bereinigung
        │   ├── analysis_page.py            : Visualisierung & Statistiken
        │   ├── price_prediction_page.py    : ML-Modul zur Preisberechnung
        │   ├── Fazit_page.py               : Fazit & Ausblick
        │   └── download_page.py            : Exportseite
        │
        └── utils/
            ├── helpers.py                  : Farbpalette & Helfer
            ├── style.py                    : CSS für Layout
            └── logo_loader.py              : Logo aus URL laden & Base64
    ```
    """)