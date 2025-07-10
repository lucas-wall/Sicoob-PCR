import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import gradio as gr
import datetime
from datetime import datetime, timedelta
import random
import base64
from io import BytesIO
import warnings
warnings.filterwarnings("ignore")

# Configuração da página
st.set_page_config(
    page_title="SICOOB - Análise de Crédito Rural",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para design moderno (será preenchido em um commit posterior)
st.markdown("""
<style>
    /* Estilos CSS serão adicionados aqui */
</style>
""", unsafe_allow_html=True)

# Função principal
def main():
    st.title("Bem-vindo ao SICOOB - Análise de Crédito Rural")
    st.write("Este é o início do seu aplicativo.")

if __name__ == "__main__":
    main()