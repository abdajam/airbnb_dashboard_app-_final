import streamlit as st
import pandas as pd

def show(logo_base64):
    st.header("CSV-Datei hochladen und Datenbereinigung") 
    uploaded_file = st.file_uploader("Lade eine CSV-Datei hoch", type=["csv"]) 

    if uploaded_file is not None: 
        try: 
            # Daten einlesen 
            data = pd.read_csv(uploaded_file) 
            # Sicherstellen, dass die Datei die richtigen Spalten enthält 
            required_columns = {'latitude', 'longitude', 'neighbourhood', 'room_type', 'price', 'minimum_nights'} 
            if required_columns.issubset(data.columns): 
                # Anzahl der Zeilen vor der Bereinigung
                total_rows_before = len(data)
                formatted_value = f"{total_rows_before:,}".replace(",", ".")
                st.info(f"Die CSV-Datei enthält {formatted_value} Zeilen.")
                # Überprüfen, ob 'neighbourhood_group' Spalte existiert
                if 'neighbourhood_group' in data.columns:
                    if data['neighbourhood_group'].isnull().all():
                        data['neighbourhood_group'] = data['neighbourhood'].copy()
                        data.drop(columns=['neighbourhood'], inplace=True)
                        st.info("Die Spalte 'neighbourhood' wurde in 'neighbourhood_group' umbenannt, da 'neighbourhood_group' leer war.")
                else:
                    data['neighbourhood_group'] = data['neighbourhood'].copy()
                    data.drop(columns=['neighbourhood'], inplace=True)
                    st.info("Die Spalte 'neighbourhood' wurde in 'neighbourhood_group' umbenannt, da 'neighbourhood_group' nicht existierte.")
                # Fehlende Werte in numerischen Spalten ersetzen
                # Ersetzen von fehlenden Werten in der 'price'-Spalte
                data.loc[:, 'price'] = data.groupby(['neighbourhood_group'])['price'].transform(lambda x: x.fillna(x.mean()))
                data.loc[:, 'price'] = data['price'].round(0).astype(int)

                # Ersetzen von fehlenden Werten in der 'minimum_nights'-Spalte
                data.loc[:, 'minimum_nights'] = data.groupby('neighbourhood_group')['minimum_nights'].transform(lambda x: x.fillna(x.mean()))
                data.loc[:, 'minimum_nights'] = data['minimum_nights'].round(0).astype(int)
                
                # Ersetzen von fehlenden Werten in den 'latitude' und 'longitude'-Spalten
                data.loc[:, 'latitude'] = data['latitude'].fillna(data['latitude'].mean())
                data.loc[:, 'longitude'] = data['longitude'].fillna(data['longitude'].mean())

                # Fehlende Werte in kategorischen Spalten ersetzen
                if 'neighbourhood' in data.columns:  
                    data.loc[:, 'neighbourhood'] = data['neighbourhood'].fillna(data['neighbourhood'].mode()[0])
                data.loc[:, 'neighbourhood_group'] = data['neighbourhood_group'].fillna(data['neighbourhood_group'].mode()[0])
                data.loc[:, 'room_type'] = data['room_type'].fillna(data['room_type'].mode()[0])
                st.success("Datenbereinigung abgeschlossen.") 
                # Bereinigte Daten in st.session_state speichern 
                st.session_state['data_cleaned'] = data 
                # Vorschau der bereinigten Daten
                st.subheader("Vorschau der bereinigten Daten")
                # st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
                st.dataframe(data.head(100), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else: 
                st.error(f"Die CSV-Datei muss die folgenden Spalten enthalten: {required_columns}") 
        except Exception as e: 
            st.error(f"Fehler beim Laden der Datei: {e}") 
    else: 
        st.info("Bitte eine CSV-Datei hochladen.")