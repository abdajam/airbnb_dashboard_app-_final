import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

from utils.helpers import AIRBNB_COLORS


class PricePredictionPage:
    def __init__(self):
        self.model = None
        self.X = None
        self.df = None

    def show(self, logo_base64):
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 2rem;">
            <img src="data:image/png;base64,{logo_base64}" style="height: 60px; margin-right: 20px;">
            <h1 style="color: {AIRBNB_COLORS['primary']}; margin: 0;">AirBnB Preisvorhersage</h1>
        </div>
        """, unsafe_allow_html=True)

        # Einführungstext
        st.write("""Möchten Sie für Ihr Airbnb einen fairen Preis entsprechend den 
        aktuellen Marktbedingungen festlegen? Dann sind Sie bei uns genau richtig! 
        Unser maschineller Lernalgorithmus schätzt den optimalen Mietpreis auf Basis von 
        vergleichbaren Airbnb-Angeboten in Ihrer Stadt.""")

        # Anweisungen zur Datendatei
        st.write("""Laden Sie dazu die CSV-Datei für Ihre Stadt unter 
        https://insideairbnb.com/get-the-data/ herunter. Achten Sie darauf, 
        die Datei mit der Bezeichnung „Detailed Listings Data“ zu verwenden.""")

        # Anleitung
        st.write("""Laden Sie die Datei hier hoch und füllen Sie anschließend das 
        Formular für Ihr Airbnb aus. Schon erhalten Sie Ihren persönlichen Preisvorschlag.""")

        uploaded_file = st.file_uploader("Lade die 'Detailed Listings Data' CSV-Datei hoch:", type=["csv"])

        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.subheader("Vorschau der Daten")
            st.write(df.head(100))

            required_columns = [
                'price', 'room_type', 'accommodates', 'bathrooms', 'bedrooms',
                'minimum_nights', 'instant_bookable', 'neighbourhood_cleansed'
            ]

            if not all(col in df.columns for col in required_columns):
                st.error("Die erforderlichen Spalten fehlen in der Datei. Bitte stelle sicher, dass alle notwendigen Spalten vorhanden sind.")
                return

            self.df = df
            self.prepare_data()
            self.train_model()
            self.evaluate_model()
            self.get_user_input_and_predict()

    def prepare_data(self):
        df = self.df
        df['room_type'] = df['room_type'].fillna('room_type')
        df['instant_bookable'] = df['instant_bookable'].fillna('instant_bookable')
        df['neighbourhood_cleansed'] = df['neighbourhood_cleansed'].fillna('neighbourhood_cleansed')
        df = df.dropna(subset=['price'])
        df['price'] = df['price'].replace({r'\$': '', ',': ''}, regex=True).astype(float)
        df = df[df['price'] > 0]
        df['log_price'] = np.log(df['price'])
        df['bathrooms'] = df['bathrooms'].fillna(df['bathrooms'].median())
        df['bedrooms'] = df['bedrooms'].fillna(df['bedrooms'].median())
        df['accommodates'] = df['accommodates'].fillna(df['accommodates'].median())
        df['minimum_nights'] = df['minimum_nights'].fillna(df['minimum_nights'].median())
        # in 'instant_bookable' ersetze 't' und 'f' durch 'Ja' und 'Nein
        df['instant_bookable'] = df['instant_bookable'].replace({'t': 'Ja', 'f': 'Nein'})

        self.X = pd.get_dummies(df[['accommodates', 'bathrooms', 'bedrooms', 'minimum_nights',
                                    'instant_bookable', 'room_type', 'neighbourhood_cleansed']], drop_first=False)
        self.df = df

    def train_model(self):
        y = self.df['log_price']
        X_train, X_test, y_train, y_test = train_test_split(self.X, y, test_size=0.2, random_state=42)

        model = LinearRegression()
        model.fit(X_train, y_train)
        self.model = model
        self.X_train, self.X_test, self.y_test = X_train, X_test, y_test

    def evaluate_model(self):
        y_pred = self.model.predict(self.X_test)
        mse = mean_squared_error(self.y_test, y_pred)
        real_mse = np.exp(mse)

        st.subheader("📈 Modellbewertung")
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Mittlerer quadratischer Fehler (Mean Squared Error: MSE)</p>
            <p class="metric-value">{real_mse:.2f}</p>
        </div>

        <div class="metric-card" style="color: red;">
            <p class="metric-label">Achtung: Der MSE (Mean Squared Error) wurde aus dem log_price wieder zurück in den ursprünglichen Price umgerechnet. Er gibt somit den mittleren quadratischen Fehler in der jeweiligen Landeswährung an.</p>
        </div>
        """, unsafe_allow_html=True)
        

    def get_user_input_and_predict(self):
        st.subheader("🔍 Dein Airbnb-Angebot")

        df = self.df
        accommodates = st.number_input("Wie viele Personen kann deine Unterkunft beherbergen?", min_value=1)
        bathrooms = st.number_input("Anzahl der Badezimmer", min_value=1)
        bedrooms = st.number_input("Anzahl der Schlafzimmer", min_value=1)
        minimum_nights = st.number_input("Minimale Aufenthaltsdauer (Nächte)", min_value=1)
        instant_bookable = st.selectbox("Sofort buchbar?", options=df['instant_bookable'].unique())
        room_type = st.selectbox("Unterkunftstyp", options=df['room_type'].unique())
        neighbourhood = st.selectbox("Stadtviertel", options=df['neighbourhood_cleansed'].unique())

        input_data = pd.DataFrame({
            'accommodates': [accommodates],
            'bathrooms': [bathrooms],
            'bedrooms': [bedrooms],
            'minimum_nights': [minimum_nights],
            'instant_bookable': [instant_bookable],
            'room_type': [room_type],
            'neighbourhood_cleansed': [neighbourhood]
        })

        input_data_dummies = pd.get_dummies(input_data, drop_first=False)
        missing_cols = set(self.X.columns) - set(input_data_dummies.columns)
        for col in missing_cols:
            input_data_dummies[col] = 0
        input_data_dummies = input_data_dummies[self.X.columns]

        prediction = self.model.predict(input_data_dummies)
        predicted_price = np.exp(prediction[0])

        st.subheader("💰 Vorhergesagter Preis")
        st.success(f"Der geschätzte Preis für dein Airbnb beträgt: **{predicted_price:.2f} ¤**")