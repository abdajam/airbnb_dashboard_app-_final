import streamlit as st
import pandas as pd
from io import BytesIO
from utils.helpers import AIRBNB_COLORS

def show(logo_base64):
    st.subheader("Danke für Deinen Besuch!")
    st.write("Wir hoffen, Dir hat die App gefallen. Nun kannst Du sie direkt über das GitHub-Repository herunterladen.") 
    st.markdown("""[Hier klicken, um die App herunterzuladen](https://github.com/abdajam/airbnb_dashboard_app-_final.git)""")
    
    # AirBnB-Stil Feedback-System mit Sternen
    st.markdown(f"""
    <div style="background-color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
        <h3 style="color: {AIRBNB_COLORS['primary']}; margin-top: 0;">Wie hat dir unsere App gefallen?</h3>
        <p style="color: {AIRBNB_COLORS['dark']};">Dein Feedback hilft uns, die App zu verbessern.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feedback-System 
    sentiment_mapping = ["1", "2", "3", "4", "5"] 
    selected = st.feedback("stars") 
    if selected is not None: 
        st.markdown(f"""
        <div style="background-color: {AIRBNB_COLORS['primary']}; color: white; padding: 10px; border-radius: 4px; text-align: center;">
            Vielen Dank für deine {sentiment_mapping[selected]} Stern(e) Bewertung!
        </div>
        """, unsafe_allow_html=True)