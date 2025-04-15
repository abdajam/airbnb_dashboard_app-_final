import streamlit as st
from utils.helpers import AIRBNB_COLORS

def show(logo_base64):
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 2rem;">
        <img src="data:image/png;base64,{logo_base64}" style="height: 60px; margin-right: 20px;">
        <h1 style="color: {AIRBNB_COLORS['primary']}; margin: 0;">Fazit & Ausblick</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## ✅ Was die App aktuell kann")
    st.markdown("""
Die AirBnB-Dashboard-App vereint **Datenanalyse**, **Visualisierung** und **Machine Learning** in einer einzigen, benutzerfreundlichen Weboberfläche:

- **Datenaufbereitung & Analyse:**
  - CSV-Upload von [insideairbnb.com](https://insideairbnb.com/get-the-data/)
  - Automatische Datenbereinigung
  - Interaktive Filter und Visualisierungen (Karten, Balken, Heatmaps, etc.)

- **Machine Learning:**
  - Preisvorhersage-Modul mit linearem Regressionsmodell
  - Individuelle Eingaben & direkte Preisprognose

- **UI & Struktur:**
  - Einheitliches AirBnB-Farbschema
  - Navigationsmenü
  - Startseite im Präsentationsstil & Projektstrukturansicht
    """)

    st.markdown("## 🚀 Ausblick: Erweiterungsmöglichkeiten")
    st.markdown("""
- **Erweiterte Analyse:**
  - Zeitreihen, Vergleich von Städten, erweiterte Filter

- **KI & Modellvergleich:**
  - Weitere ML-Modelle (z. B. XGBoost)
  - Feature-Importance-Analyse

- **Business-Funktionen:**
  - Umsatzschätzungen
  - Investitionsanalyse & Empfehlungen

- **UX-Verbesserungen:**
  - Mehrsprachigkeit
  - Nutzerführung & Speicherung
    """)
