import streamlit as st
import google.generativeai as genai

# 1. Configuração da Página
st.set_page_config(
    page_title="Validador SENAI",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Estilização CSS Personalizada (Cores no Padrão SENAI)
st.markdown("""
    
""", unsafe_allow_html=True)

# 3. Cabeçalho do App
st.markdown('
