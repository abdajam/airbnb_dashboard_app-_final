AirBnB Insights & Preisvorhersage Dashboard
===========================================

Dieses Projekt ist ein interaktives Streamlit-Dashboard zur Analyse und Preisprognose von AirBnB-Angeboten
auf Basis öffentlich verfügbarer Daten von http://insideairbnb.com.

🔍 Hauptfunktionen
--------------------
- Upload & Bereinigung von AirBnB-CSV-Daten
- Interaktive Filter und Visualisierungen (z.B. Karten, Histogramme)
- Statistische Auswertungen (Durchschnittspreise, Verteilung)
- Download als Excel-Datei
- Maschinelles Lernen zur Preisvorhersage basierend auf Nutzerangaben

🧠 Genutzte Technologien
--------------------------
- Python 3
- Streamlit
- Pandas, NumPy
- scikit-learn
- Plotly, Pydeck

📂 Projektstruktur
--------------------
app/
├── main.py                # Einstiegspunkt
├── controller.py          # AppController-Klasse
├── pages/
│   ├── home_page.py
│   ├── info_page.py
│   ├── upload_page.py
│   ├── analysis_page.py
│   ├── download_page.py
│   ├── structure_page.py
│   ├── price_prediction_page.py
│   └── fazit_page.py
└── utils/
    ├── helpers.py
    ├── style.py
    └── logo_loader.py

🚀 Projekt ausführen
----------------------
1. Repository klonen:
   git clone https://github.com/abdajam/airbnb_dashboard_app-_final

2. In Projektordner wechseln:
   cd airbnb-dashboard

3. Virtual Environment erstellen (optional aber empfohlen):
   python -m venv venv
   source venv/bin/activate  # Windows: venv\\Scripts\\activate

4. Abhängigkeiten installieren:
   pip install -r requirements.txt

5. App starten:
   streamlit run app/main.py

📌 Hinweis
----------
- CSV-Dateien müssen bestimmte Spalten enthalten (siehe Info-Seite im Dashboard).
- Empfohlene Datenquelle: https://insideairbnb.com/get-the-data/

🛠 Autor
--------
Dieses Projekt wurde im Rahmen eines Data-Science-Abschlussprojekts von "Abdelmounaim Ajam" und "Tim Köhler" erstellt.