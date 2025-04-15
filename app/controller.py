import streamlit as st
from my_pages import info_page, upload_page, analysis_page, download_page
from utils.style import apply_custom_style
from utils.logo_loader import load_logo_base64
from utils.helpers import AIRBNB_COLORS
from my_pages import home_page, structure_page
from my_pages.price_prediction_page import PricePredictionPage
from my_pages import fazit_page

class AppController:
    def __init__(self):
        st.set_page_config(
            page_title="AirBnB Insights Dashboard",
            page_icon="🏠",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        apply_custom_style()
        self.logo_base64 = load_logo_base64()
        self.pages = {
            "🏠 Home": home_page.show,
            "📂 Programmstruktur": structure_page.show,
            "ℹ️ Info": info_page.show,
            "📤 CSV-Datei hochladen": upload_page.show,
            "📈 Statistiken und Visualisierungen": analysis_page.show,
            "📱 Preisvorhersage": PricePredictionPage().show,
            "📌 Fazit & Ausblick": fazit_page.show,
            "🫂 Danke und App herunterladen": download_page.show,
        }
        if 'page' not in st.session_state:
            st.session_state['page'] = "🏠 Home"  # Standardwert setzen
    def run(self):
        self.render_header()
        self.render_sidebar()
        selected_page = st.session_state['page']
        self.pages[selected_page](self.logo_base64)
    def render_header(self):
        st.markdown(f"""
        <div class="header-container">
            <img src="data:image/png;base64,{self.logo_base64}" class="logo" alt="AirBnB Logo">
            <h1 class="header-title">AirBnB Insights Dashboard</h1>
        </div>
        """, unsafe_allow_html=True)
    def render_sidebar(self):
        st.sidebar.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <img src="data:image/png;base64,{self.logo_base64}" style="width: 120px; margin-bottom: 10px;">
            <h3 style="color: {AIRBNB_COLORS['primary']}; margin: 0;">AirBnB Insights</h3>
        </div>
        """, unsafe_allow_html=True)
        st.sidebar.markdown(
            f"<h3 style='color: {AIRBNB_COLORS['dark']}; border-bottom: 1px solid #e6e6e6; padding-bottom: 10px;'>Navigation</h3>",
            unsafe_allow_html=True
        )
        page = st.sidebar.selectbox("Wähle eine Seite:", list(self.pages.keys()))
        st.session_state['page'] = page