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


# Função para criar gráficos
def create_charts(df):
    charts = {}

    # Evolução do Volume de Crédito Rural (Mensal)
    df_monthly = df.set_index(\'data_operacao\').resample(\'M\')[\\'valor_operacao\\'].sum().reset_index()
    df_monthly.columns = [\\'Período\\', \\'Volume (R$)\\']
    charts[\\'volume_evolution\'] = px.line(df_monthly, x=\'Período\', y=\'Volume (R$)\', 
                                         title=\'Evolução do Volume de Crédito Rural\',
                                         labels={\'Volume (R$)\': \'Volume (R$)\'},
                                         color_discrete_sequence=[\\'#006341\\'])
    charts[\\'volume_evolution\\'].update_layout(hovermode=\'x unified\', template=\'plotly_white\')

    # Volume por Linha de Crédito
    df_linha = df.groupby(\'linha_credito\')[\\'valor_operacao\\'].sum().reset_index()
    df_linha = df_linha.sort_values(\'valor_operacao\', ascending=False)
    charts[\\'volume_linha\'] = px.bar(df_linha, x=\'linha_credito\', y=\'valor_operacao\', 
                                      title=\'Volume por Linha de Crédito\',
                                      labels={\'valor_operacao\': \'Volume (R$)\'},
                                      color_discrete_sequence=[\\'#00A0DF\\'])
    charts[\\'volume_linha\\'].update_layout(hovermode=\'x unified\', template=\'plotly_white\')

    # Distribuição Regional do Volume
    df_regiao = df.groupby(\'regiao\')[\\'valor_operacao\\'].sum().reset_index()
    df_regiao = df_regiao.sort_values(\'valor_operacao\', ascending=False)
    charts[\\'volume_regiao\'] = px.pie(df_regiao, names=\'regiao\', values=\'valor_operacao\', 
                                       title=\'Distribuição Regional do Volume\',
                                       color_discrete_sequence=px.colors.sequential.Teal)
    charts[\\'volume_regiao\\'].update_traces(textinfo=\'percent+label\', pull=[0.05]*len(df_regiao))

    # Volume por Cultura
    df_cultura = df.groupby(\'cultura\')[\\'valor_operacao\\'].sum().reset_index()
    df_cultura = df_cultura.sort_values(\'valor_operacao\', ascending=False)
    charts[\\'volume_cultura\'] = px.bar(df_cultura, x=\'cultura\', y=\'valor_operacao\', 
                                        title=\'Volume por Cultura\',
                                        labels={\'valor_operacao\': \'Volume (R$)\'},
                                        color_discrete_sequence=[\\'#006341\\'])
    charts[\\'volume_cultura\\'].update_layout(hovermode=\'x unified\', template=\'plotly_white\')

    return charts

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
    
    # Sidebar com filtros
    st.sidebar.markdown("## 🔍 Filtros")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input("Data Inicial", value=datetime(2024, 1, 1))
    with col2:
        end_date = st.date_input("Data Final", value=datetime(2024, 12, 31))

    selected_linhas = st.sidebar.multiselect(
        "Linhas de Crédito",
        df[\\'linha_credito\\'].unique(),
        default=df[\\'linha_credito\\'].unique()
    )
    selected_regioes = st.sidebar.multiselect(
        "Regiões",
        df[\\'regiao\\'].unique(),
        default=df[\\'regiao\\'].unique()
    )
    selected_culturas = st.sidebar.multiselect(
        "Culturas",
        df[\\'cultura\\'].unique(),
        default=df[\\'cultura\\'].unique()
    )
    
    # Aplicar filtros
    mask = (
        (df[\\'data_operacao\\'] >= pd.Timestamp(start_date)) &
        (df[\\'data_operacao\\'] <= pd.Timestamp(end_date)) &
        (df[\\'linha_credito\\'].isin(selected_linhas)) &
        (df[\\'regiao\\'].isin(selected_regioes)) &
        (df[\\'cultura\\'].isin(selected_culturas))
    )
    df_filtered = df[mask]
    
    # KPIs
    kpis = calculate_kpis(df_filtered)
    
    st.markdown("## 📊 Indicadores Principais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        delta_color = "normal" if kpis[\\'volume_change\\'] >= 0 else "inverse"
        st.metric(
            label="Volume Total da Carteira",
            value=format_currency(kpis[\\'total_volume\\]),
            delta=f"{kpis[\\'volume_change\\']:.1f}%"
        )
    
    with col2:
        delta_color = "normal" if kpis[\\'operacoes_change\\'] >= 0 else "inverse"
        st.metric(
            label="Total de Operações",
            value=format_number(kpis[\\'total_operacoes\\]),
            delta=f"{kpis[\\'operacoes_change\\']:.1f}%"
        )
    
    with col3:
        delta_color = "normal" if kpis[\\'ticket_change\\'] >= 0 else "inverse"
        st.metric(
            label="Ticket Médio",
            value=format_currency(kpis[\\'ticket_medio\\]),
            delta=f"{kpis[\\'ticket_change\\']:.1f}%"
        )
    
    with col4:
        delta_color = "inverse" if kpis[\\'inadimplencia_change\\'] >= 0 else "normal"
        st.metric(
            label="Taxa de Inadimplência",
            value=f"{kpis[\\'taxa_inadimplencia\\']:.1f}%",
            delta=f"{kpis[\\'inadimplencia_change\\']:.1f}pp"
        )

    # Gráficos
    st.markdown("## 📈 Análises Temporais e por Produto")
    charts = create_charts(df_filtered)
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(charts[\\'volume_evolution\\'], use_container_width=True)
    with col2:
        st.plotly_chart(charts[\\'volume_linha\\'], use_container_width=True)

    st.markdown("## 🗺️ Análises Regionais e por Cultura")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(charts[\\'volume_regiao\\'], use_container_width=True)
    with col2:
        st.plotly_chart(charts[\\'volume_cultura\\'], use_container_width=True)

    st.markdown("## 📋 Dados Detalhados")
    st.dataframe(df_filtered)

# Função principal que gerencia as páginas
def main():
    # Navegação
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