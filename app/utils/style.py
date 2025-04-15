import streamlit as st

def apply_custom_style():
    st.markdown("""
    <style>
    body {
        background-color: #f7f7f7;
    }
    .header-title {
        color: #FF5A5F;
        font-size: 2.5rem;
        font-weight: 700;
    }
    .logo {
        height: 40px;
        margin-right: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)