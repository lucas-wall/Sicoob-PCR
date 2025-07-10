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

# Função para gerar dados simulados
@st.cache_data
def generate_sample_data():
    """Gera dados simulados para o dashboard"""
    np.random.seed(42)
    
    # Dados de operações de crédito rural
    dates = pd.date_range(start=\'2023-01-01\', end=\'2024-12-31\', freq=\'D\')
    n_operations = len(dates) * 5  # 5 operações por dia em média
    
    data = {
        \'data_operacao\': np.random.choice(dates, n_operations),
        \'valor_operacao\': np.random.lognormal(mean=10, sigma=1, size=n_operations),
        \'linha_credito\': np.random.choice([\'Custeio\', \'Investimento\', \'Comercialização\', \'Pronaf\'], n_operations),
        \'cultura\': np.random.choice([\'Soja\', \'Milho\', \'Café\', \'Cana-de-açúcar\', \'Algodão\'], n_operations),
        \'regiao\': np.random.choice([\'Centro-Oeste\', \'Sudeste\', \'Sul\', \'Nordeste\', \'Norte\'], n_operations),
        \'cooperativa\': np.random.choice([f\'Cooperativa {i}\' for i in range(1, 21)], n_operations),
        \'taxa_juros\': np.random.normal(8.5, 2, n_operations),
        \'prazo_meses\': np.random.choice([6, 12, 18, 24, 36, 48, 60], n_operations),
        \'status\': np.random.choice([\'Adimplente\', \'Inadimplente\'], n_operations, p=[0.92, 0.08])
    }
    
    df = pd.DataFrame(data)
    df[\'valor_operacao\'] = np.clip(df[\'valor_operacao\'], 1000, 5000000)
    df[\'taxa_juros\'] = np.clip(df[\'taxa_juros\'], 3, 15)
    
    return df

# Função para calcular KPIs
def calculate_kpis(df):
    """Calcula os principais KPIs"""
    total_volume = df[\'valor_operacao\'].sum()
    total_operacoes = len(df)
    ticket_medio = df[\'valor_operacao\'].mean()
    taxa_inadimplencia = (df[\'status\'] == \'Inadimplente\').mean() * 100
    
    # Calcular variações (simuladas)
    volume_change = random.uniform(-5, 15)
    operacoes_change = random.uniform(-3, 12)
    ticket_change = random.uniform(-8, 10)
    inadimplencia_change = random.uniform(-2, 3)
    
    return {
        \'total_volume\': total_volume,
        \'total_operacoes\': total_operacoes,
        \'ticket_medio\': ticket_medio,
        \'taxa_inadimplencia\': taxa_inadimplencia,
        \'volume_change\': volume_change,
        \'operacoes_change\': operacoes_change,
        \'ticket_change\': ticket_change,
        \'inadimplencia_change\': inadimplencia_change
    }

# Função para formatação de valores
def format_currency(value):
    """Formata valores em moeda brasileira"""
    if value >= 1e9:
        return f"R$ {value/1e9:.1f}B"
    elif value >= 1e6:
        return f"R$ {value/1e6:.1f}M"
    elif value >= 1e3:
        return f"R$ {value/1e3:.1f}K"
    else:
        return f"R$ {value:.0f}"

def format_number(value):
    """Formata números grandes"""
    if value >= 1e6:
        return f"{value/1e6:.1f}M"
    elif value >= 1e3:
        return f"{value/1e3:.1f}K"
    else:
        return f"{value:.0f}"

# Função principal do Streamlit
def main_dashboard():
    # Header
    st.markdown("""
    <div class=\"header-container\">
        <h1 class=\"header-title\">🌾 SICOOB - Análise de Crédito Rural</h1>
        <p class=\"header-subtitle\">Dashboard Executivo para Gestão Estratégica da Carteira</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Carregar dados
    df = generate_sample_data()
    
    # Sidebar com filtros (apenas data por enquanto)
    st.sidebar.markdown("## 🔍 Filtros")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input("Data Inicial", value=datetime(2024, 1, 1))
    with col2:
        end_date = st.date_input("Data Final", value=datetime(2024, 12, 31))
    
    # Aplicar filtros
    mask = (
        (df[\'data_operacao\'] >= pd.Timestamp(start_date)) &
        (df[\'data_operacao\'] <= pd.Timestamp(end_date))
    )
    df_filtered = df[mask]
    
    # KPIs
    kpis = calculate_kpis(df_filtered)
    
    st.markdown("## 📊 Indicadores Principais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        delta_color = "normal" if kpis[\'volume_change\'] >= 0 else "inverse"
        st.metric(
            label="Volume Total da Carteira",
            value=format_currency(kpis[\'total_volume\']),
            delta=f"{kpis[\'volume_change\']:.1f}%"
        )
    
    with col2:
        delta_color = "normal" if kpis[\'operacoes_change\'] >= 0 else "inverse"
        st.metric(
            label="Total de Operações",
            value=format_number(kpis[\'total_operacoes\']),
            delta=f"{kpis[\'operacoes_change\']:.1f}%"
        )
    
    with col3:
        delta_color = "normal" if kpis[\'ticket_change\'] >= 0 else "inverse"
        st.metric(
            label="Ticket Médio",
            value=format_currency(kpis[\'ticket_medio\']),
            delta=f"{kpis[\'ticket_change\']:.1f}%"
        )
    
    with col4:
        delta_color = "inverse" if kpis[\'inadimplencia_change\'] >= 0 else "normal"
        st.metric(
            label="Taxa de Inadimplência",
            value=f"{kpis[\'taxa_inadimplencia\']:.1f}%",
            delta=f"{kpis[\'inadimplencia_change\']:.1f}pp"
        )

# Função principal que gerencia as páginas
def main():
    # Navegação (apenas dashboard por enquanto)
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 🧭 Navegação")
    
    page = st.sidebar.selectbox(
        "Escolha uma seção:",
        ["📊 Dashboard Principal"]
    )
    
    if page == "📊 Dashboard Principal":
        main_dashboard()

if __name__ == "__main__":
    main()