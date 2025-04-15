import streamlit as st

def show(logo_base64):
    st.header("Information zur Datenbereinigung und Nutzung der App") 
    st.write(""" 
    Diese Anwendung bietet einen umfassenden Überblick über AirBnB-Immobilien.
             
    Hier findest du Daten zu verschiedenen Städten, aus denen du eine beliebige Stadt deiner Wahl darstellen kannst. Klicke einfach auf den angegebenen Link, um die entsprechenden CSV-Dateien herunterzuladen.
             
    Es gibt zwei Varianten der Listingsdaten: eine detaillierte Version als `gz` ZIP-Datei und die zusammengefasste `listings.csv`, welche für unsere Zwecke besser geeignet ist. 
    Wähle also bitte nicht die `listings.csv.gz`, sondern die `listings.csv` Datei.          
    """)
    st.markdown("""[Hier klicken, um Beispiel-CSV-Dateien herunterzuladen](https://insideairbnb.com/get-the-data/)""")

    st.write("""
    Die Verarbeitung erfolgt abhängig von der jeweiligen Stadt, für die Daten im CSV-Format bereitgestellt wurden. Dabei werden diese Schritte umgesetzt: 
    1. **Datenbereinigung**: 
        - Fehlende Werte in den Spalten `price`, `minimum_nights`, `latitude` und `longitude` werden durch den Mittelwert oder Median der 'neighbourhood_group' ersetzt, um die Datenintegrität zu gewährleisten.
        - Die Spalte ‚neighbourhood‘ wird in ‚neighbourhood_group‘ umbenannt, sofern letztere nicht bereits im Datensatz vorhanden ist.
        - Fehlende Werte in den kategorischen Spalten `neighbourhood`, `neighbourhood_group` und `room_type` werden durch den häufigsten Wert (Modus) ersetzt.
    2. **Erwartete Spalten**: 
        - Die CSV-Datei sollte die folgenden Spalten enthalten: 
            - `latitude`: Breitengrad der Immobilie 
            - `longitude`: Längengrad der Immobilie 
            - `neighbourhood`: Name der Nachbarschaft 
            - `neighbourhood_group`: Gruppe der Nachbarschaft (optional) 
            - `room_type`: Art des Zimmers 
            - `price`: Preis der Immobilie 
    3. **Output**: 
        - Nach der Bereinigung der Daten können Statistiken und Visualisierungen angezeigt werden.
    """)