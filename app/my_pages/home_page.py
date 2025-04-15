import streamlit as st
from utils.helpers import AIRBNB_COLORS

def show(logo_base64):
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 2rem;">
        <h1 style="color: {AIRBNB_COLORS['primary']}; margin: 0; font-size: 3rem;">Data-Science-Institute - DSI</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background-color: {AIRBNB_COLORS['primary']}; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
        <h2 style="color: {AIRBNB_COLORS['dark']}">Abschlussprojekt</h2>
        <p style="font-size: 18px; margin-top: 10px;">
            <strong>Thema:</strong> Analyse von Airbnb-Daten zur Entscheidungsunterstützung<br>
            <strong>Projektcrew:</strong> Abdelmounaim Ajam, Tim Köhler<br>
            <strong>Datum:</strong> 17. April 2025
        </p>
    </div>
    """, unsafe_allow_html=True)