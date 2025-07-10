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

# CSS personalizado para design moderno
st.markdown("""
<style>
    /* Importar fontes */
    @import url("https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" );
    
    /* Reset e configurações globais */
    .main {
        font-family: "Inter", sans-serif;
        background: linear-gradient(135deg, #333333 0%, #1a1a1a 100%);
    }
    
    /* Header personalizado */
    .header-container {
        background: linear-gradient(90deg, #006341 0%, #00A0DF 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 99, 65, 0.2);
    }
    
    .header-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
    }
    
    .header-subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2rem;
        font-weight: 400;
        text-align: center;
        margin-top: 0.5rem;
    }
    
    /* Cards de KPI */
    .kpi-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(0, 99, 65, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 1rem;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 99, 65, 0.15);
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #006341;
        margin: 0;
    }
    
    .kpi-label {
        font-size: 1rem;
        color: #666;
        font-weight: 500;
        margin-top: 0.5rem;
    }
    
    .kpi-change {
        font-size: 0.9rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    .kpi-change.positive {
        color: #10B981;
    }
    
    .kpi-change.negative {
        color: #EF4444;
    }
    
    /* Seções */
    .section-container {
        background: linear-gradient(90deg, #006341 0%, #00A0DF 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        margin-bottom: 2rem;
        border: 1px solid rgba(0, 99, 65, 0.05);
    }
    
    .section-title {
        color: #006341;
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Filtros */
    .filter-container {
        background: rgba(0, 99, 65, 0.05);
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid rgba(0, 99, 65, 0.1);
    }
    
    /* Botões */
    .stButton > button {
        background: linear-gradient(90deg, #006341 0%, #00A0DF 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 99, 65, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 99, 65, 0.3);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #006341 0%, #00A0DF 100%);
    }
    
    /* Métricas do Streamlit */
    [data-testid="metric-container"] {
        background: white;
        border: 1px solid rgba(0, 99, 65, 0.1);
        padding: 1rem;
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    
    /* Gráficos */
    .js-plotly-plot {
        border-radius: 16px;
        overflow: hidden;
    }
    
    /* Gradio container */
    .gradio-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        margin-top: 2rem;
    }
    
    /* Esconder elementos do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Responsividade */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2rem;
        }
        
        .kpi-value {
            font-size: 2rem;
        }
        
        .section-container {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Função para gerar dados simulados
@st.cache_data
def generate_sample_data():
    """Gera dados simulados para o dashboard"""
    np.random.seed(42)
    
    # Dados de operações de crédito rural
    dates = pd.date_range(start="2023-01-01", end="2024-12-31", freq="D")
    n_operations = len(dates) * 5  # 5 operações por dia em média
    
    data = {
        "data_operacao": np.random.choice(dates, n_operations),
        "valor_operacao": np.random.lognormal(mean=10, sigma=1, size=n_operations),
        "linha_credito": np.random.choice(["Custeio", "Investimento", "Comercialização", "Pronaf"], n_operations),
        "cultura": np.random.choice(["Soja", "Milho", "Café", "Cana-de-açúcar", "Algodão"], n_operations),
        "regiao": np.random.choice(["Centro-Oeste", "Sudeste", "Sul", "Nordeste", "Norte"], n_operations),
        "cooperativa": np.random.choice([f"Cooperativa {i}" for i in range(1, 21)], n_operations),
        "taxa_juros": np.random.normal(8.5, 2, n_operations),
        "prazo_meses": np.random.choice([6, 12, 18, 24, 36, 48, 60], n_operations),
        "status": np.random.choice(["Adimplente", "Inadimplente"], n_operations, p=[0.92, 0.08])
    }
    
    df = pd.DataFrame(data)
    df["valor_operacao"] = np.clip(df["valor_operacao"], 1000, 5000000)
    df["taxa_juros"] = np.clip(df["taxa_juros"], 3, 15)
    
    return df

# Função para calcular KPIs
def calculate_kpis(df):
    """Calcula os principais KPIs"""
    total_volume = df["valor_operacao"].sum()
    total_operacoes = len(df)
    ticket_medio = df["valor_operacao"].mean()
    taxa_inadimplencia = (df["status"] == "Inadimplente").mean() * 100
    
    # Calcular variações (simuladas)
    volume_change = random.uniform(-5, 15)
    operacoes_change = random.uniform(-3, 12)
    ticket_change = random.uniform(-8, 10)
    inadimplencia_change = random.uniform(-2, 3)
    
    return {
        "total_volume": total_volume,
        "total_operacoes": total_operacoes,
        "ticket_medio": ticket_medio,
        "taxa_inadimplencia": taxa_inadimplencia,
        "volume_change": volume_change,
        "operacoes_change": operacoes_change,
        "ticket_change": ticket_change,
        "inadimplencia_change": inadimplencia_change
    }

# Função para criar gráficos
def create_charts(df):
    """Cria os gráficos do dashboard"""
    charts = {}
    
    # 1. Evolução temporal do volume
    df_monthly = df.groupby(df["data_operacao"].dt.to_period("M"))["valor_operacao"].sum().reset_index()
    df_monthly["data_operacao"] = df_monthly["data_operacao"].astype(str)
    
    fig_evolution = px.line(
        df_monthly, 
        x="data_operacao", 
        y="valor_operacao",
        title="Evolução do Volume de Crédito Rural",
        labels={"valor_operacao": "Volume (R$)", "data_operacao": "Período"}
    )
    fig_evolution.update_traces(line_color="#006341", line_width=3)
    fig_evolution.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_family="Inter",
        title_font_size=20,
        title_font_color="#006341"
    )
    charts["evolution"] = fig_evolution
    
    # 2. Volume por linha de crédito
    df_linha = df.groupby("linha_credito")["valor_operacao"].sum().reset_index()
    
    fig_linha = px.bar(
        df_linha,
        x="linha_credito",
        y="valor_operacao",
        title="Volume por Linha de Crédito",
        color="valor_operacao",
        color_continuous_scale=["#00A0DF", "#006341"]
    )
    fig_linha.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_family="Inter",
        title_font_size=20,
        title_font_color="#006341",
        showlegend=False
    )
    charts["linha_credito"] = fig_linha
    
    # 3. Distribuição por região
    df_regiao = df.groupby("regiao")["valor_operacao"].sum().reset_index()
    
    fig_regiao = px.pie(
        df_regiao,
        values="valor_operacao",
        names="regiao",
        title="Distribuição Regional do Volume",
        color_discrete_sequence=["#006341", "#00A0DF", "#4CAF50", "#FF9800", "#9C27B0"]
    )
    fig_regiao.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_family="Inter",
        title_font_size=20,
        title_font_color="#006341"
    )
    charts["regiao"] = fig_regiao
    
    # 4. Volume por cultura
    df_cultura = df.groupby("cultura")["valor_operacao"].sum().reset_index()
    
    fig_cultura = px.bar(
        df_cultura,
        x="cultura",
        y="valor_operacao",
        title="Volume por Cultura",
        color="valor_operacao",
        color_continuous_scale=["#00A0DF", "#006341"]
    )
    fig_cultura.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_family="Inter",
        title_font_size=20,
        title_font_color="#006341",
        showlegend=False
    )
    charts["cultura"] = fig_cultura
    
    return charts

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
    <div class="header-container">
        <h1 class="header-title">🌾 SICOOB - Análise de Crédito Rural</h1>
        <p class="header-subtitle">Dashboard Executivo para Gestão Estratégica da Carteira</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Carregar dados
    df = generate_sample_data()
    
    # Sidebar com filtros
    st.sidebar.markdown("## 🔍 Filtros")
    
    # Filtro de período
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input("Data Inicial", value=datetime(2024, 1, 1))
    with col2:
        end_date = st.date_input("Data Final", value=datetime(2024, 12, 31))
    
    # Filtros adicionais
    linhas_credito = st.sidebar.multiselect(
        "Linhas de Crédito",
        options=df["linha_credito"].unique(),
        default=df["linha_credito"].unique()
    )
    
    regioes = st.sidebar.multiselect(
        "Regiões",
        options=df["regiao"].unique(),
        default=df["regiao"].unique()
    )
    
    culturas = st.sidebar.multiselect(
        "Culturas",
        options=df["cultura"].unique(),
        default=df["cultura"].unique()
    )
    
    # Aplicar filtros
    mask = (
        (df["data_operacao"] >= pd.Timestamp(start_date)) &
        (df["data_operacao"] <= pd.Timestamp(end_date)) &
        (df["linha_credito"].isin(linhas_credito)) &
        (df["regiao"].isin(regioes)) &
        (df["cultura"].isin(culturas))
    )
    df_filtered = df[mask]
    
    # KPIs
    kpis = calculate_kpis(df_filtered)
    
    st.markdown("## 📊 Indicadores Principais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        delta_color = "normal" if kpis["volume_change"] >= 0 else "inverse"
        st.metric(
            label="Volume Total da Carteira",
            value=format_currency(kpis["total_volume"]),
            delta=f"{kpis["volume_change"]:+.1f}%"
        )
    
    with col2:
        delta_color = "normal" if kpis["operacoes_change"] >= 0 else "inverse"
        st.metric(
            label="Total de Operações",
            value=format_number(kpis["total_operacoes"]),
            delta=f"{kpis["operacoes_change"]:+.1f}%"
        )
    
    with col3:
        delta_color = "normal" if kpis["ticket_change"] >= 0 else "inverse"
        st.metric(
            label="Ticket Médio",
            value=format_currency(kpis["ticket_medio"]),
            delta=f"{kpis["ticket_change"]:+.1f}%"
        )
    
    with col4:
        delta_color = "inverse" if kpis["inadimplencia_change"] >= 0 else "normal"
        st.metric(
            label="Taxa de Inadimplência",
            value=f"{kpis["taxa_inadimplencia"]:.1f}%",
            delta=f"{kpis["inadimplencia_change"]:+.1f}pp"
        )
    
    # Gráficos
    charts = create_charts(df_filtered)
    
    # Primeira linha de gráficos
    st.markdown("## 📈 Análises Temporais e por Produto")
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(charts["evolution"], use_container_width=True)
    
    with col2:
        st.plotly_chart(charts["linha_credito"], use_container_width=True)
    
    # Segunda linha de gráficos
    st.markdown("## 🗺️ Análises Regionais e por Cultura")
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(charts["regiao"], use_container_width=True)
    
    with col2:
        st.plotly_chart(charts["cultura"], use_container_width=True)
    
    # Tabela de dados
    st.markdown("## 📋 Dados Detalhados")
    
    # Preparar dados para exibição
    df_display = df_filtered.copy()
    df_display["valor_operacao"] = df_display["valor_operacao"].apply(lambda x: f"R$ {x:,.2f}")
    df_display["taxa_juros"] = df_display["taxa_juros"].apply(lambda x: f"{x:.2f}%")
    df_display["data_operacao"] = df_display["data_operacao"].dt.strftime("%d/%m/%Y")
    
    # Renomear colunas
    df_display = df_display.rename(columns={
        "data_operacao": "Data",
        "valor_operacao": "Valor",
        "linha_credito": "Linha de Crédito",
        "cultura": "Cultura",
        "regiao": "Região",
        "cooperativa": "Cooperativa",
        "taxa_juros": "Taxa de Juros",
        "prazo_meses": "Prazo (meses)",
        "status": "Status"
    })
    
    st.dataframe(
        df_display.head(100),
        use_container_width=True,
        hide_index=True
    )

# Função de previsão com Gradio
def create_prediction_interface():
    """Cria interface de previsão com Gradio"""
    
    def predict_default_risk(valor_operacao, taxa_juros, prazo_meses, linha_credito, cultura, regiao):
        """Simula uma previsão de risco de inadimplência"""
        
        # Simulação de modelo preditivo
        base_risk = 0.08  # 8% de risco base
        
        # Ajustes baseados nos parâmetros
        if valor_operacao > 1000000:
            base_risk += 0.02
        elif valor_operacao < 50000:
            base_risk -= 0.01
            
        if taxa_juros > 12:
            base_risk += 0.03
        elif taxa_juros < 6:
            base_risk -= 0.01
            
        if prazo_meses > 36:
            base_risk += 0.015
            
        # Ajustes por linha de crédito
        linha_adjustments = {
            "Custeio": -0.005,
            "Investimento": 0.01,
            "Comercialização": -0.01,
            "Pronaf": -0.02
        }
        base_risk += linha_adjustments.get(linha_credito, 0)
        
        # Ajustes por cultura
        cultura_adjustments = {
            "Soja": -0.01,
            "Milho": -0.005,
            "Café": 0.005,
            "Cana-de-açúcar": 0.01,
            "Algodão": 0.015
        }
        base_risk += cultura_adjustments.get(cultura, 0)
        
        # Ajustes por região
        regiao_adjustments = {
            "Centro-Oeste": -0.01,
            "Sul": -0.005,
            "Sudeste": 0,
            "Nordeste": 0.02,
            "Norte": 0.015
        }
        base_risk += regiao_adjustments.get(regiao, 0)
        
        # Garantir que o risco esteja entre 0 e 1
        risk_probability = max(0, min(1, base_risk))
        
        # Classificação de risco
        if risk_probability < 0.05:
            risk_class = "Baixo Risco"
            color = "🟢"
        elif risk_probability < 0.15:
            risk_class = "Risco Moderado"
            color = "🟡"
        else:
            risk_class = "Alto Risco"
            color = "🔴"
        
        # Recomendações
        recommendations = []
        if risk_probability > 0.15:
            recommendations.append("• Considerar garantias adicionais")
            recommendations.append("• Revisar capacidade de pagamento")
            recommendations.append("• Monitoramento mensal obrigatório")
        elif risk_probability > 0.05:
            recommendations.append("• Monitoramento trimestral")
            recommendations.append("• Verificar histórico de crédito")
        else:
            recommendations.append("• Cliente elegível para condições preferenciais")
            recommendations.append("• Monitoramento semestral")
        
        result = f"""
        ## {color} Análise de Risco de Crédito
        
        **Probabilidade de Inadimplência:** {risk_probability:.2%}
        
        **Classificação:** {risk_class}
        
        **Valor da Operação:** R$ {valor_operacao:,.2f}
        **Taxa de Juros:** {taxa_juros:.2f}% a.a.
        **Prazo:** {prazo_meses} meses
        
        ### Recomendações:
        {chr(10).join(recommendations)}
        
        ### Fatores de Risco Considerados:
        • Valor da operação
        • Taxa de juros aplicada
        • Prazo de financiamento
        • Linha de crédito
        • Tipo de cultura
        • Região geográfica
        """
        
        return result
    
    # Interface Gradio
    with gr.Blocks(
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            font-family: "Inter", sans-serif;
        }
        .gr-button-primary {
            background: linear-gradient(90deg, #006341 0%, #00A0DF 100%);
            border: none;
        }
        """
    ) as interface:
        
        gr.Markdown("""
        # 🤖 Sistema de Previsão de Risco - SICOOB
        ### Análise Preditiva para Operações de Crédito Rural
        """)
        
        with gr.Row():
            with gr.Column():
                valor_operacao = gr.Number(
                    label="Valor da Operação (R$)",
                    value=100000,
                    minimum=1000,
                    maximum=10000000
                )
                
                taxa_juros = gr.Slider(
                    label="Taxa de Juros (% a.a.)",
                    minimum=3,
                    maximum=20,
                    value=8.5,
                    step=0.1
                )
                
                prazo_meses = gr.Slider(
                    label="Prazo (meses)",
                    minimum=6,
                    maximum=60,
                    value=24,
                    step=6
                )
            
            with gr.Column():
                linha_credito = gr.Dropdown(
                    label="Linha de Crédito",
                    choices=["Custeio", "Investimento", "Comercialização", "Pronaf"],
                    value="Custeio"
                )
                
                cultura = gr.Dropdown(
                    label="Cultura",
                    choices=["Soja", "Milho", "Café", "Cana-de-açúcar", "Algodão"],
                    value="Soja"
                )
                
                regiao = gr.Dropdown(
                    label="Região",
                    choices=["Centro-Oeste", "Sudeste", "Sul", "Nordeste", "Norte"],
                    value="Centro-Oeste"
                )
        
        predict_btn = gr.Button("🔍 Analisar Risco", variant="primary", size="lg")
        
        output = gr.Markdown(label="Resultado da Análise")
        
        predict_btn.click(
            fn=predict_default_risk,
            inputs=[valor_operacao, taxa_juros, prazo_meses, linha_credito, cultura, regiao],
            outputs=output
        )
        
        gr.Markdown("""
        ---
        **Nota:** Este é um modelo demonstrativo para fins educacionais. 
        Em produção, seria utilizado um modelo de machine learning treinado com dados históricos reais.
        """)
    
    return interface

# Função principal
def main():
    # Navegação
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 🧭 Navegação")
    
    page = st.sidebar.selectbox(
        "Escolha uma seção:",
        ["📊 Dashboard Principal", "🤖 Previsão de Risco", "📄 Sobre o Sistema"]
    )
    
    if page == "📊 Dashboard Principal":
        main_dashboard()
        
    elif page == "🤖 Previsão de Risco":
        st.markdown("""
        <div class="header-container">
            <h1 class="header-title">🤖 Sistema de Previsão de Risco</h1>
            <p class="header-subtitle">Análise Preditiva para Operações de Crédito Rural</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="section-container">
            <p style="font-size: 1.1rem; color: white; text-align: center; margin-bottom: 2rem;">
                Utilize nossa ferramenta de inteligência artificial para avaliar o risco de inadimplência 
                de operações de crédito rural. Insira os parâmetros da operação e obtenha uma análise 
                detalhada com recomendações personalizadas.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Integrar Gradio no Streamlit
        interface = create_prediction_interface()
        
        # Renderizar interface Gradio usando iframe
        st.markdown("### 🤖 Interface de Previsão de Risco")
        st.markdown("""
        <div style="background: linear-gradient(90deg, #006341 0%, #00A0DF 100%); padding: 2rem; border-radius: 16px; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);">
            <p style="text-align: center; color: white; margin-bottom: 1rem;">
                A interface de previsão será carregada abaixo. Caso não apareça, 
                <a href="http://localhost:7860" target="_blank">clique aqui para abrir em nova aba</a>.
            </p>
        </div>
        """, unsafe_allow_html=True )
        
        # Tentar renderizar o Gradio de forma mais simples
        try:
            # Criar uma versão simplificada da previsão diretamente no Streamlit
            st.markdown("### 📊 Simulador de Risco Simplificado")
            
            col1, col2 = st.columns(2)
            
            with col1:
                valor_op = st.number_input("Valor da Operação (R$)", min_value=1000, max_value=10000000, value=100000)
                taxa_juros = st.slider("Taxa de Juros (% a.a.)", min_value=3.0, max_value=20.0, value=8.5, step=0.1)
                prazo = st.slider("Prazo (meses)", min_value=6, max_value=60, value=24, step=6)
            
            with col2:
                linha = st.selectbox("Linha de Crédito", ["Custeio", "Investimento", "Comercialização", "Pronaf"])
                cultura = st.selectbox("Cultura", ["Soja", "Milho", "Café", "Cana-de-açúcar", "Algodão"])
                regiao = st.selectbox("Região", ["Centro-Oeste", "Sudeste", "Sul", "Nordeste", "Norte"])
            
            if st.button("🔍 Analisar Risco", type="primary"):
                # Simulação de análise de risco
                base_risk = 0.08
                
                if valor_op > 1000000:
                    base_risk += 0.02
                elif valor_op < 50000:
                    base_risk -= 0.01
                    
                if taxa_juros > 12:
                    base_risk += 0.03
                elif taxa_juros < 6:
                    base_risk -= 0.01
                    
                if prazo > 36:
                    base_risk += 0.015
                
                linha_adj = {"Custeio": -0.005, "Investimento": 0.01, "Comercialização": -0.01, "Pronaf": -0.02}
                base_risk += linha_adj.get(linha, 0)
                
                cultura_adj = {"Soja": -0.01, "Milho": -0.005, "Café": 0.005, "Cana-de-açúcar": 0.01, "Algodão": 0.015}
                base_risk += cultura_adj.get(cultura, 0)
                
                regiao_adj = {"Centro-Oeste": -0.01, "Sul": -0.005, "Sudeste": 0, "Nordeste": 0.02, "Norte": 0.015}
                base_risk += regiao_adj.get(regiao, 0)
                
                risk_prob = max(0, min(1, base_risk))
                
                if risk_prob < 0.05:
                    risk_class = "Baixo Risco"
                    color = "🟢"
                elif risk_prob < 0.15:
                    risk_class = "Risco Moderado"
                    color = "🟡"
                else:
                    risk_class = "Alto Risco"
                    color = "🔴"
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Probabilidade de Inadimplência", f"{risk_prob:.2%}")
                
                with col2:
                    st.metric("Classificação", f"{color} {risk_class}")
                
                with col3:
                    st.metric("Valor da Operação", f"R$ {valor_op:,.2f}")
                
                st.success(f"Análise concluída! Operação classificada como {risk_class}.")
                
        except Exception as e:
            st.error(f"Erro ao carregar interface de previsão: {str(e)}")
            st.info("Funcionalidade de previsão em desenvolvimento.")
        
    elif page == "📄 Sobre o Sistema":
        st.markdown("""
        <div class="header-container">
            <h1 class="header-title">📄 Sobre o Sistema</h1>
            <p class="header-subtitle">Informações Técnicas e Metodologia</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="section-container">
                <h3 style="color: white;">🎯 Objetivo</h3>
                <p>Este sistema foi desenvolvido para demonstrar capacidades avançadas de análise de dados 
                e modelagem preditiva aplicadas ao setor de crédito rural do SICOOB.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="section-container">
                <h3 style="color: white;">🛠️ Tecnologias Utilizadas</h3>
                <ul>
                    <li><strong>Streamlit:</strong> Interface web interativa</li>
                    <li><strong>Gradio:</strong> Interface de machine learning</li>
                    <li><strong>Plotly:</strong> Visualizações interativas</li>
                    <li><strong>Pandas:</strong> Manipulação de dados</li>
                    <li><strong>NumPy:</strong> Computação numérica</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="section-container">
                <h3 style="color: white;">📊 Funcionalidades</h3>
                <ul>
                    <li>Dashboard executivo com KPIs principais</li>
                    <li>Análises temporais e geográficas</li>
                    <li>Filtros interativos avançados</li>
                    <li>Sistema de previsão de risco</li>
                    <li>Interface responsiva e moderna</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="section-container">
                <h3 style="color: white;">🔮 Modelo Preditivo</h3>
                <p>O modelo de previsão considera múltiplos fatores:</p>
                <ul>
                    <li>Valor e prazo da operação</li>
                    <li>Taxa de juros aplicada</li>
                    <li>Linha de crédito e cultura</li>
                    <li>Localização geográfica</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="section-container">
            <h3 style="color: white; text-align: center;">👨‍💻 Desenvolvido para o Processo Seletivo SICOOB</h3>
            <p style="text-align: center; font-size: 1.1rem; color: white;">
                Este sistema demonstra competências em análise de dados, desenvolvimento de interfaces 
                modernas e aplicação de técnicas de machine learning no contexto do agronegócio.
            </p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()