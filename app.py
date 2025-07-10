import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
import base64
from io import BytesIO
import markdown
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
import re
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="SICOOB - Análise de Crédito Rural",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para o tema SICOOB
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #006341 0%, #00A0DF 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #006341;
    }
    
    .insight-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #00A0DF;
        margin: 1rem 0;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #006341 0%, #00A0DF 100%);
    }
    
    .stSelectbox > div > div {
        background-color: linear-gradient(180deg, #006341 0%, #00A0DF 100%);
    }
</style>
""", unsafe_allow_html=True)

# Função para criar PDF formatado
def create_pdf_report(report_content, report_type):
    """Cria um PDF formatado a partir do conteúdo markdown"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Estilos
    styles = getSampleStyleSheet()
    
    # Estilos personalizados SICOOB
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.HexColor('#006341'),
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.HexColor('#006341'),
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=10,
        spaceBefore=15,
        textColor=colors.HexColor('#00A0DF'),
        fontName='Helvetica-Bold'
    )
    
    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=8,
        spaceBefore=12,
        textColor=colors.HexColor('#006341'),
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    )
    
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=4,
        leftIndent=20,
        fontName='Helvetica'
    )
    
    # Processar conteúdo markdown
    story = []
    
    # Header do documento
    story.append(Paragraph("🌾 SICOOB - Sistema de Cooperativas de Crédito do Brasil", title_style))
    story.append(Paragraph(f"{report_type}", heading1_style))
    story.append(Spacer(1, 20))
    
    # Processar linhas do markdown
    lines = report_content.split('\n')
    current_list = []
    
    for line in lines:
        line = line.strip()
        
        if not line:
            if current_list:
                # Finalizar lista atual
                for item in current_list:
                    story.append(Paragraph(f"• {item}", bullet_style))
                current_list = []
            story.append(Spacer(1, 6))
            continue
        
        # Títulos
        if line.startswith('# '):
            if current_list:
                for item in current_list:
                    story.append(Paragraph(f"• {item}", bullet_style))
                current_list = []
            title_text = line[2:].strip()
            story.append(Paragraph(title_text, heading1_style))
            
        elif line.startswith('## '):
            if current_list:
                for item in current_list:
                    story.append(Paragraph(f"• {item}", bullet_style))
                current_list = []
            subtitle_text = line[3:].strip()
            story.append(Paragraph(subtitle_text, heading2_style))
            
        elif line.startswith('### '):
            if current_list:
                for item in current_list:
                    story.append(Paragraph(f"• {item}", bullet_style))
                current_list = []
            subsubtitle_text = line[4:].strip()
            story.append(Paragraph(subsubtitle_text, heading3_style))
            
        # Listas
        elif line.startswith('- ') or line.startswith('* '):
            item_text = line[2:].strip()
            # Processar formatação em negrito
            item_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', item_text)
            current_list.append(item_text)
            
        # Texto normal
        else:
            if current_list:
                for item in current_list:
                    story.append(Paragraph(f"• {item}", bullet_style))
                current_list = []
            
            if line:
                # Processar formatação em negrito
                line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
                story.append(Paragraph(line, body_style))
    
    # Finalizar lista pendente
    if current_list:
        for item in current_list:
            story.append(Paragraph(f"• {item}", bullet_style))
    
    # Footer
    story.append(Spacer(1, 30))
    story.append(Paragraph("___", body_style))
    story.append(Paragraph(f"Relatório gerado automaticamente pelo Sistema de Análise SICOOB", body_style))
    story.append(Paragraph(f"Data de geração: {datetime.now().strftime('%d/%m/%Y às %H:%M')}", body_style))
    
    # Construir PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

# Função para gerar dados sintéticos realistas
@st.cache_data
def generate_synthetic_data():
    np.random.seed(42)
    
    # Dados históricos da carteira (últimos 24 meses)
    dates = pd.date_range(start='2023-01-01', end='2025-06-30', freq='M')
    
    # Dados por região
    regioes_data = {
        'Centro-Oeste': {'volume': 18500, 'cooperativas': 145, 'inadimplencia': 5.9, 'participacao': 0.34},
        'Sul': {'volume': 16200, 'cooperativas': 178, 'inadimplencia': 6.1, 'participacao': 0.30},
        'Sudeste': {'volume': 12800, 'cooperativas': 156, 'inadimplencia': 6.8, 'participacao': 0.24},
        'Nordeste': {'volume': 4200, 'cooperativas': 89, 'inadimplencia': 8.2, 'participacao': 0.08},
        'Norte': {'volume': 2000, 'cooperativas': 34, 'inadimplencia': 7.5, 'participacao': 0.04}
    }
    
    # Gerar dados históricos por região
    carteira_historica_completa = []
    
    for regiao, dados_regiao in regioes_data.items():
        base_volume = dados_regiao['volume']
        base_inadimplencia = dados_regiao['inadimplencia']
        
        # Volume com sazonalidade específica por região
        seasonal_factor = np.sin(np.arange(len(dates)) * 2 * np.pi / 12) * 0.15 + 1
        growth_trend = np.linspace(1, 1.25, len(dates))
        volume_regional = base_volume * seasonal_factor * growth_trend + np.random.normal(0, base_volume * 0.02, len(dates))
        
        # Inadimplência com variação regional
        inadimplencia_regional = np.random.normal(base_inadimplencia, 0.8, len(dates)).clip(3, 12)
        
        # Número de operações baseado no volume
        operacoes_regional = (volume_regional / 150 + np.random.normal(0, 20, len(dates))).astype(int)
        
        for i, date in enumerate(dates):
            carteira_historica_completa.append({
                'Data': date,
                'Regiao': regiao,
                'Volume_Milhoes': volume_regional[i],
                'Inadimplencia': inadimplencia_regional[i],
                'Numero_Operacoes': operacoes_regional[i]
            })
    
    carteira_historica = pd.DataFrame(carteira_historica_completa)
    
    # Dados por linha de crédito (agora com distribuição regional)
    linhas_credito = {}
    linhas_base = {
        'Custeio': {'participacao': 60, 'inadimplencia_base': 6.2},
        'Investimento': {'participacao': 22, 'inadimplencia_base': 5.8},
        'Comercialização': {'participacao': 12, 'inadimplencia_base': 7.1},
        'Industrialização': {'participacao': 6, 'inadimplencia_base': 6.9}
    }
    
    for linha, dados_linha in linhas_base.items():
        linhas_credito[linha] = {}
        for regiao, dados_regiao in regioes_data.items():
            volume_linha_regiao = dados_regiao['volume'] * (dados_linha['participacao'] / 100)
            inadimplencia_linha = dados_linha['inadimplencia_base'] + (dados_regiao['inadimplencia'] - 6.5) * 0.3
            
            linhas_credito[linha][regiao] = {
                'volume': volume_linha_regiao,
                'inadimplencia': inadimplencia_linha
            }
    
    # Dados de culturas por região
    culturas_base = {
        'Soja': {'area_mil_ha': 4200, 'inadimplencia_base': 5.8},
        'Milho': {'area_mil_ha': 2800, 'inadimplencia_base': 6.2},
        'Café': {'area_mil_ha': 1900, 'inadimplencia_base': 6.9},
        'Cana-de-açúcar': {'area_mil_ha': 850, 'inadimplencia_base': 7.1},
        'Algodão': {'area_mil_ha': 720, 'inadimplencia_base': 6.5}
    }
    
    # Distribuição de culturas por região (percentuais aproximados)
    distribuicao_culturas = {
        'Centro-Oeste': {'Soja': 0.45, 'Milho': 0.35, 'Café': 0.05, 'Cana-de-açúcar': 0.10, 'Algodão': 0.05},
        'Sul': {'Soja': 0.40, 'Milho': 0.30, 'Café': 0.15, 'Cana-de-açúcar': 0.10, 'Algodão': 0.05},
        'Sudeste': {'Soja': 0.20, 'Milho': 0.25, 'Café': 0.35, 'Cana-de-açúcar': 0.15, 'Algodão': 0.05},
        'Nordeste': {'Soja': 0.15, 'Milho': 0.20, 'Café': 0.10, 'Cana-de-açúcar': 0.25, 'Algodão': 0.30},
        'Norte': {'Soja': 0.25, 'Milho': 0.30, 'Café': 0.20, 'Cana-de-açúcar': 0.15, 'Algodão': 0.10}
    }
    
    culturas_data = {}
    for cultura, dados_cultura in culturas_base.items():
        culturas_data[cultura] = {}
        for regiao, dados_regiao in regioes_data.items():
            participacao_cultura = distribuicao_culturas[regiao][cultura]
            volume_cultura_regiao = dados_regiao['volume'] * participacao_cultura
            area_cultura_regiao = dados_cultura['area_mil_ha'] * participacao_cultura
            inadimplencia_cultura = dados_cultura['inadimplencia_base'] + (dados_regiao['inadimplencia'] - 6.5) * 0.2
            
            culturas_data[cultura][regiao] = {
                'volume': volume_cultura_regiao,
                'area_mil_ha': area_cultura_regiao,
                'inadimplencia': inadimplencia_cultura
            }
    
    return carteira_historica, linhas_credito, regioes_data, culturas_data

# Funções para filtrar dados por região
def filter_carteira_by_region(carteira_df, regioes_selecionadas):
    """Filtra dados da carteira pelas regiões selecionadas"""
    if not regioes_selecionadas or len(regioes_selecionadas) == 0:
        return carteira_df
    
    carteira_filtrada = carteira_df[carteira_df['Regiao'].isin(regioes_selecionadas)]
    
    # Agregar dados por data
    carteira_agregada = carteira_filtrada.groupby('Data').agg({
        'Volume_Milhoes': 'sum',
        'Inadimplencia': 'mean',
        'Numero_Operacoes': 'sum'
    }).reset_index()
    
    return carteira_agregada

def filter_linhas_credito_by_region(linhas_credito, regioes_selecionadas):
    """Filtra dados de linhas de crédito pelas regiões selecionadas"""
    if not regioes_selecionadas or len(regioes_selecionadas) == 0:
        return linhas_credito
    
    linhas_filtradas = {}
    for linha, dados_linha in linhas_credito.items():
        volume_total = 0
        inadimplencia_ponderada = 0
        
        for regiao in regioes_selecionadas:
            if regiao in dados_linha:
                volume_regiao = dados_linha[regiao]['volume']
                volume_total += volume_regiao
                inadimplencia_ponderada += dados_linha[regiao]['inadimplencia'] * volume_regiao
        
        if volume_total > 0:
            inadimplencia_media = inadimplencia_ponderada / volume_total
            linhas_filtradas[linha] = {
                'volume': volume_total,
                'inadimplencia': inadimplencia_media
            }
    
    # Calcular participações
    volume_total_geral = sum([dados['volume'] for dados in linhas_filtradas.values()])
    for linha in linhas_filtradas:
        linhas_filtradas[linha]['participacao'] = (linhas_filtradas[linha]['volume'] / volume_total_geral) * 100
    
    return linhas_filtradas

def filter_regioes_data_by_region(regioes_data, regioes_selecionadas):
    """Filtra dados regionais pelas regiões selecionadas"""
    if not regioes_selecionadas or len(regioes_selecionadas) == 0:
        return regioes_data
    
    return {regiao: dados for regiao, dados in regioes_data.items() if regiao in regioes_selecionadas}

def filter_culturas_by_region(culturas_data, regioes_selecionadas):
    """Filtra dados de culturas pelas regiões selecionadas"""
    if not regioes_selecionadas or len(regioes_selecionadas) == 0:
        return culturas_data
    
    culturas_filtradas = {}
    for cultura, dados_cultura in culturas_data.items():
        volume_total = 0
        area_total = 0
        inadimplencia_ponderada = 0
        
        for regiao in regioes_selecionadas:
            if regiao in dados_cultura:
                volume_regiao = dados_cultura[regiao]['volume']
                area_regiao = dados_cultura[regiao]['area_mil_ha']
                volume_total += volume_regiao
                area_total += area_regiao
                inadimplencia_ponderada += dados_cultura[regiao]['inadimplencia'] * volume_regiao
        
        if volume_total > 0:
            inadimplencia_media = inadimplencia_ponderada / volume_total
            culturas_filtradas[cultura] = {
                'volume': volume_total,
                'area_mil_ha': area_total,
                'inadimplencia': inadimplencia_media
            }
    
    return culturas_filtradas

# Função para criar gráficos
def create_volume_evolution_chart(df):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['Data'],
        y=df['Volume_Milhoes'],
        mode='lines+markers',
        name='Volume da Carteira',
        line=dict(color='#006341', width=3),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title='Evolução do Volume da Carteira de Crédito Rural',
        xaxis_title='Período',
        yaxis_title='Volume (R$ Milhões)',
        template='plotly_white',
        height=400
    )
    
    return fig

def create_inadimplencia_chart(df):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['Data'],
        y=df['Inadimplencia'],
        mode='lines+markers',
        name='Taxa de Inadimplência',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=6)
    ))
    
    # Linha de meta (7%)
    fig.add_hline(y=7.0, line_dash="dash", line_color="red", 
                  annotation_text="Meta: 7%")
    
    fig.update_layout(
        title='Evolução da Taxa de Inadimplência',
        xaxis_title='Período',
        yaxis_title='Taxa de Inadimplência (%)',
        template='plotly_white',
        height=400
    )
    
    return fig

def create_linhas_credito_chart(linhas_data):
    labels = list(linhas_data.keys())
    values = [linhas_data[linha]['volume'] for linha in labels]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker_colors=['#006341', '#00A0DF', '#4CAF50', '#FF9800']
    )])
    
    fig.update_layout(
        title='Distribuição por Linha de Crédito',
        height=400
    )
    
    return fig

def create_regional_analysis(regioes_data):
    regioes = list(regioes_data.keys())
    volumes = [regioes_data[regiao]['volume'] for regiao in regioes]
    inadimplencia = [regioes_data[regiao]['inadimplencia'] for regiao in regioes]
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Volume por Região', 'Inadimplência por Região'),
        specs=[[{"type": "bar"}, {"type": "bar"}]]
    )
    
    fig.add_trace(
        go.Bar(x=regioes, y=volumes, name='Volume (R$ Mi)', 
               marker_color='#006341'),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(x=regioes, y=inadimplencia, name='Inadimplência (%)', 
               marker_color='#FF6B6B'),
        row=1, col=2
    )
    
    fig.update_layout(height=400, showlegend=False)
    
    return fig

# Função principal
def main():
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🌾 SICOOB - Análise Estratégica de Crédito Rural</h1>
        <p>Dashboard Executivo para Gestão da Carteira Rural</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Carregar dados
    carteira_df, linhas_credito, regioes_data, culturas_data = generate_synthetic_data()
    
    # Sidebar
    st.sidebar.markdown("## 🎛️ Controles do Dashboard")
    
    # Filtros
    periodo_inicio = st.sidebar.date_input(
        "Data Início",
        value=datetime(2024, 1, 1),
        min_value=datetime(2023, 1, 1),
        max_value=datetime(2025, 6, 30)
    )
    
    periodo_fim = st.sidebar.date_input(
        "Data Fim",
        value=datetime(2025, 6, 30),
        min_value=datetime(2023, 1, 1),
        max_value=datetime(2025, 6, 30)
    )
    
    regiao_filtro = st.sidebar.multiselect(
        "Selecionar Regiões",
        options=list(regioes_data.keys()),
        default=list(regioes_data.keys())
    )
    
    # Aplicar filtros regionais
    carteira_filtrada_regiao = filter_carteira_by_region(carteira_df, regiao_filtro)
    linhas_credito_filtradas = filter_linhas_credito_by_region(linhas_credito, regiao_filtro)
    regioes_data_filtradas = filter_regioes_data_by_region(regioes_data, regiao_filtro)
    culturas_data_filtradas = filter_culturas_by_region(culturas_data, regiao_filtro)
    
    # Filtrar dados por período
    mask = (carteira_filtrada_regiao['Data'] >= pd.to_datetime(periodo_inicio)) & \
           (carteira_filtrada_regiao['Data'] <= pd.to_datetime(periodo_fim))
    carteira_filtrada = carteira_filtrada_regiao.loc[mask]
    
    # Mostrar filtros ativos
    if len(regiao_filtro) < len(regioes_data):
        st.sidebar.info(f"🔍 Filtro ativo: {', '.join(regiao_filtro)}")
        
        # Mostrar impacto dos filtros
        volume_total_original = sum([dados['volume'] for dados in regioes_data.values()])
        volume_total_filtrado = sum([dados['volume'] for dados in regioes_data_filtradas.values()])
        percentual_filtrado = (volume_total_filtrado / volume_total_original) * 100
        
        st.sidebar.metric(
            "Volume Filtrado", 
            f"R$ {volume_total_filtrado:,.0f} Mi",
            f"{percentual_filtrado:.1f}% do total"
        )
    else:
        st.sidebar.success("📊 Exibindo todas as regiões")
    
    # Indicador visual de filtros ativos na página principal
    if len(regiao_filtro) < len(regioes_data):
        st.info(f"🔍 **Filtros Ativos:** Exibindo dados para {', '.join(regiao_filtro)} | "
                f"Período: {periodo_inicio.strftime('%d/%m/%Y')} a {periodo_fim.strftime('%d/%m/%Y')}")
    
    # KPIs principais
    st.markdown("## 📊 Indicadores Principais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        volume_atual = carteira_filtrada['Volume_Milhoes'].iloc[-1]
        volume_anterior = carteira_filtrada['Volume_Milhoes'].iloc[-2] if len(carteira_filtrada) > 1 else volume_atual
        delta_volume = ((volume_atual - volume_anterior) / volume_anterior) * 100
        
        st.metric(
            label="Volume da Carteira",
            value=f"R$ {volume_atual:,.0f} Mi",
            delta=f"{delta_volume:+.1f}%"
        )
    
    with col2:
        inadimplencia_atual = carteira_filtrada['Inadimplencia'].iloc[-1]
        inadimplencia_anterior = carteira_filtrada['Inadimplencia'].iloc[-2] if len(carteira_filtrada) > 1 else inadimplencia_atual
        delta_inadimplencia = inadimplencia_atual - inadimplencia_anterior
        
        st.metric(
            label="Taxa de Inadimplência",
            value=f"{inadimplencia_atual:.1f}%",
            delta=f"{delta_inadimplencia:+.1f}pp",
            delta_color="inverse"
        )
    
    with col3:
        total_operacoes = carteira_filtrada['Numero_Operacoes'].sum()
        st.metric(
            label="Total de Operações",
            value=f"{total_operacoes:,}"
        )
    
    with col4:
        ticket_medio = volume_atual * 1000000 / carteira_filtrada['Numero_Operacoes'].iloc[-1]
        st.metric(
            label="Ticket Médio",
            value=f"R$ {ticket_medio:,.0f}"
        )
    
    # Gráficos principais
    st.markdown("## 📈 Análise Temporal")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_volume = create_volume_evolution_chart(carteira_filtrada)
        st.plotly_chart(fig_volume, use_container_width=True)
    
    with col2:
        fig_inadimplencia = create_inadimplencia_chart(carteira_filtrada)
        st.plotly_chart(fig_inadimplencia, use_container_width=True)
    
    # Análise por segmentos
    st.markdown("## 🎯 Análise por Segmentos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_linhas = create_linhas_credito_chart(linhas_credito_filtradas)
        st.plotly_chart(fig_linhas, use_container_width=True)
    
    with col2:
        fig_regional = create_regional_analysis(regioes_data_filtradas)
        st.plotly_chart(fig_regional, use_container_width=True)
    
    # Insights e Recomendações
    st.markdown("## 💡 Insights e Recomendações")
    
    # Gerar insights baseados nos dados filtrados
    volume_total_filtrado = sum([dados['volume'] for dados in regioes_data_filtradas.values()])
    inadimplencia_media_filtrada = sum([dados['inadimplencia'] * dados['volume'] for dados in regioes_data_filtradas.values()]) / volume_total_filtrado if volume_total_filtrado > 0 else 0
    
    # Identificar região com maior volume nas regiões filtradas
    regiao_maior_volume = max(regioes_data_filtradas.items(), key=lambda x: x[1]['volume']) if regioes_data_filtradas else None
    
    # Identificar cultura com maior volume nas culturas filtradas
    cultura_maior_volume = max(culturas_data_filtradas.items(), key=lambda x: x[1]['volume']) if culturas_data_filtradas else None
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("🎯 **Oportunidades Identificadas**")
        insights_oportunidades = []
        
        if regiao_maior_volume:
            insights_oportunidades.append(f"**Foco em {regiao_maior_volume[0]}:** Região representa R$ {regiao_maior_volume[1]['volume']:,.0f} Mi do volume filtrado")
        
        if cultura_maior_volume:
            insights_oportunidades.append(f"**Especialização em {cultura_maior_volume[0]}:** Cultura com maior volume (R$ {cultura_maior_volume[1]['volume']:,.0f} Mi)")
        
        if inadimplencia_media_filtrada < 6.5:
            insights_oportunidades.append("**Baixo Risco:** Taxa de inadimplência abaixo da média nacional")
        
        insights_oportunidades.extend([
            "**Digitalização:** 78% dos produtores demandam soluções digitais integradas",
            "**Produtos ESG:** Crescimento de 45% na demanda por crédito sustentável"
        ])
        
        for insight in insights_oportunidades:
            st.markdown(insight)
    
    with col2:
        st.warning("⚠️ **Pontos de Atenção**")
        insights_atencao = []
        
        if inadimplencia_media_filtrada > 7.0:
            insights_atencao.append(f"**Alta Inadimplência:** Taxa média de {inadimplencia_media_filtrada:.1f}% nas regiões selecionadas")
        
        if len(regiao_filtro) == 1:
            insights_atencao.append("**Concentração Regional:** Análise focada em apenas uma região")
        
        insights_atencao.extend([
            "**Sazonalidade:** Picos de demanda em março e setembro exigem planejamento",
            "**Risco Climático:** Impacto crescente nas taxas de inadimplência",
            "**Concorrência:** Bancos digitais e fintechs ganhando market share"
        ])
        
        for insight in insights_atencao:
            st.markdown(insight)
    
    # Simulador de Cenários
    st.markdown("## 🔮 Simulador de Cenários")
    
    with st.expander("Configurar Simulação"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            crescimento_carteira = st.slider("Crescimento da Carteira (%)", -10, 30, 12)
        
        with col2:
            meta_inadimplencia = st.slider("Meta de Inadimplência (%)", 3.0, 10.0, 6.5)
        
        with col3:
            investimento_digital = st.slider("Investimento Digital (R$ Mi)", 0, 500, 150)
        
        # Calcular projeções
        volume_projetado = volume_atual * (1 + crescimento_carteira/100)
        economia_inadimplencia = (inadimplencia_atual - meta_inadimplencia) * volume_projetado * 0.01
        roi_digital = investimento_digital * 2.3  # ROI estimado de 230%
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Volume Projetado", f"R$ {volume_projetado:,.0f} Mi")
        
        with col2:
            st.metric("Economia c/ Inadimplência", f"R$ {economia_inadimplencia:,.0f} Mi")
        
        with col3:
            st.metric("ROI Digital", f"R$ {roi_digital:,.0f} Mi")
    
    # Análise de Culturas
    st.markdown("## 🌱 Análise por Cultura")
    
    culturas_df = pd.DataFrame(culturas_data_filtradas).T
    culturas_df.reset_index(inplace=True)
    culturas_df.rename(columns={'index': 'Cultura'}, inplace=True)
    
    fig_culturas = px.scatter(
        culturas_df,
        x='area_mil_ha',
        y='volume',
        size='volume',
        color='inadimplencia',
        hover_name='Cultura',
        labels={
            'area_mil_ha': 'Área Plantada (Mil Ha)',
            'volume': 'Volume de Crédito (R$ Mi)',
            'inadimplencia': 'Inadimplência (%)'
        },
        title='Relação entre Área Plantada, Volume de Crédito e Inadimplência',
        color_continuous_scale='RdYlGn_r'
    )
    
    st.plotly_chart(fig_culturas, use_container_width=True)
    
    # Modelo Preditivo
    st.markdown("## 🤖 Modelo Preditivo de Credit Scoring")
    
    # Usar session_state para manter os valores
    if 'scoring_calculated' not in st.session_state:
        st.session_state.scoring_calculated = False
    
    with st.expander("Simular Credit Scoring", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Dados do Produtor")
            idade = st.number_input("Idade", 18, 80, 45, key="idade_input")
            experiencia = st.number_input("Anos de Experiência", 0, 50, 15, key="exp_input")
            area_propriedade = st.number_input("Área da Propriedade (Ha)", 1, 10000, 500, key="area_input")
            cultura_principal = st.selectbox("Cultura Principal", list(culturas_data_filtradas.keys()) if culturas_data_filtradas else list(culturas_data.keys()), key="cultura_input")
            regiao = st.selectbox("Região", regiao_filtro if regiao_filtro else list(regioes_data.keys()), key="regiao_input")
        
        with col2:
            st.subheader("Dados Financeiros")
            renda_anual = st.number_input("Renda Anual (R$ mil)", 50, 10000, 800, key="renda_input")
            valor_solicitado = st.number_input("Valor Solicitado (R$ mil)", 10, 5000, 300, key="valor_input")
            garantias = st.selectbox("Tipo de Garantia", ["Real", "Fidejussória", "Mista"], key="garantia_input")
            historico_pagamento = st.selectbox("Histórico", ["Excelente", "Bom", "Regular", "Ruim"], key="historico_input")
        
        if st.button("🎯 Calcular Score", type="primary"):
            # Algoritmo simplificado de credit scoring
            score_base = 600
            
            # Fatores de ajuste
            score_idade = min(20, (idade - 25) * 0.5) if idade > 25 else 0
            score_experiencia = min(30, experiencia * 2)
            score_area = min(25, np.log(area_propriedade) * 5)
            score_renda = min(40, np.log(renda_anual) * 8)
            
            # Penalizações por risco
            if cultura_principal in culturas_data_filtradas:
                risco_cultura = culturas_data_filtradas[cultura_principal]['inadimplencia']
            else:
                # Fallback para dados originais se não houver dados filtrados
                risco_cultura = 6.5  # Valor médio
            
            if regiao in regioes_data_filtradas:
                risco_regiao = regioes_data_filtradas[regiao]['inadimplencia']
            else:
                risco_regiao = 6.5  # Valor médio
            
            score_risco = -((risco_cultura + risco_regiao) * 2)
            
            # Histórico
            historico_scores = {"Excelente": 50, "Bom": 30, "Regular": 10, "Ruim": -30}
            score_historico = historico_scores[historico_pagamento]
            
            # Score final
            score_final = score_base + score_idade + score_experiencia + score_area + score_renda + score_risco + score_historico
            score_final = max(300, min(850, score_final))  # Limitar entre 300-850
            
            # Salvar no session_state
            st.session_state.score_final = score_final
            st.session_state.scoring_calculated = True
            
            # Classificação
            if score_final >= 750:
                classificacao = "Excelente"
                taxa_sugerida = "CDI + 2%"
                st.session_state.classificacao = classificacao
                st.session_state.taxa_sugerida = taxa_sugerida
            elif score_final >= 650:
                classificacao = "Bom"
                taxa_sugerida = "CDI + 4%"
                st.session_state.classificacao = classificacao
                st.session_state.taxa_sugerida = taxa_sugerida
            elif score_final >= 550:
                classificacao = "Regular"
                taxa_sugerida = "CDI + 6%"
                st.session_state.classificacao = classificacao
                st.session_state.taxa_sugerida = taxa_sugerida
            else:
                classificacao = "Alto Risco"
                taxa_sugerida = "CDI + 10%"
                st.session_state.classificacao = classificacao
                st.session_state.taxa_sugerida = taxa_sugerida
        
        # Mostrar resultados se calculado
        if st.session_state.scoring_calculated:
            st.markdown("### 📊 Resultado da Análise")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Score de Crédito", f"{st.session_state.score_final:.0f}")
            
            with col2:
                if st.session_state.score_final >= 750:
                    st.success(f"**Classificação:** {st.session_state.classificacao}")
                elif st.session_state.score_final >= 650:
                    st.info(f"**Classificação:** {st.session_state.classificacao}")
                elif st.session_state.score_final >= 550:
                    st.warning(f"**Classificação:** {st.session_state.classificacao}")
                else:
                    st.error(f"**Classificação:** {st.session_state.classificacao}")
            
            with col3:
                st.metric("Taxa Sugerida", st.session_state.taxa_sugerida)
    
    # Relatórios
    st.markdown("## 📋 Relatórios Executivos")
    
    def generate_performance_report(carteira_df, linhas_credito, regioes_data, regioes_filtro):
        """Gera relatório de performance em markdown"""
        volume_atual = carteira_df['Volume_Milhoes'].iloc[-1]
        inadimplencia_atual = carteira_df['Inadimplencia'].iloc[-1]
        crescimento = ((volume_atual - carteira_df['Volume_Milhoes'].iloc[0]) / carteira_df['Volume_Milhoes'].iloc[0]) * 100
        
        # Informações sobre filtros aplicados
        filtros_info = ""
        if len(regioes_filtro) < 5:  # Assumindo 5 regiões totais
            filtros_info = f"\n- **Regiões Analisadas:** {', '.join(regioes_filtro)}"
        
        report = f"""
# SICOOB - Relatório de Performance da Carteira Rural

## Resumo Executivo
- **Data do Relatório:** {datetime.now().strftime('%d/%m/%Y')}
- **Período Analisado:** {periodo_inicio.strftime('%d/%m/%Y')} a {periodo_fim.strftime('%d/%m/%Y')}{filtros_info}

## Indicadores Principais
- **Volume da Carteira:** R$ {volume_atual:,.0f} milhões
- **Taxa de Inadimplência:** {inadimplencia_atual:.1f}%
- **Crescimento no Período:** {crescimento:+.1f}%
- **Total de Operações:** {carteira_df['Numero_Operacoes'].sum():,}

## Performance por Linha de Crédito
"""
        for linha, dados in linhas_credito.items():
            report += f"- **{linha}:** R$ {dados['volume']:,.0f} Mi ({dados['participacao']:.1f}% da carteira)\n"
        
        report += f"""

## Distribuição Regional
"""
        for regiao, dados in regioes_data.items():
            report += f"- **{regiao}:** R$ {dados['volume']:,.0f} Mi ({dados['cooperativas']} cooperativas)\n"
        
        report += f"""

## Insights e Recomendações
### Oportunidades
- Expansão no Nordeste com potencial de crescimento de 150%
- Digitalização para atender 78% dos produtores que demandam soluções digitais
- Produtos ESG com crescimento de 45% na demanda

### Pontos de Atenção
- Concentração geográfica de 65% da carteira no Centro-Oeste e Sul
- Sazonalidade com picos em março e setembro
- Impacto crescente do risco climático

## Conclusões
O SICOOB mantém posição sólida no mercado de crédito rural, com oportunidades claras de expansão e necessidade de adaptação às tendências digitais e sustentáveis.

---
*Relatório gerado automaticamente pelo Sistema de Análise SICOOB*
        """
        return report
    
    def generate_market_analysis_report(regioes_data, culturas_data):
        """Gera relatório de análise de mercado"""
        report = f"""
# SICOOB - Análise de Mercado Rural

## Resumo Executivo
- **Data do Relatório:** {datetime.now().strftime('%d/%m/%Y')}
- **Posicionamento:** 2º lugar no ranking nacional
- **Market Share:** 22% (crescimento de 4pp em 4 anos)

## Análise Competitiva
- **Banco do Brasil:** 35% (líder de mercado)
- **SICOOB:** 22% (2º posição)
- **Sicredi:** 18% (3º posição)
- **Demais:** 25%

## Oportunidades por Região
"""
        for regiao, dados in regioes_data.items():
            potencial = dados.get('potencial', 'Médio')
            report += f"- **{regiao}:** {potencial} potencial (R$ {dados['volume']:,} Mi atual)\n"
        
        report += f"""

## Análise por Cultura
"""
        for cultura, dados in culturas_data.items():
            report += f"- **{cultura}:** R$ {dados['volume']:,} Mi ({dados['area']:,} mil ha)\n"
        
        report += f"""

## Tendências do Mercado
- Crescimento anual médio: 12%
- Digitalização acelerada pós-pandemia
- Demanda crescente por produtos ESG
- Concentração em grandes players

## Recomendações Estratégicas
1. Expansão agressiva no Nordeste
2. Investimento em tecnologia digital
3. Desenvolvimento de produtos sustentáveis
4. Parcerias estratégicas no Norte

---
*Análise de Mercado - Sistema SICOOB*
        """
        return report
    
    def generate_strategic_projections_report(volume_atual, inadimplencia_atual):
        """Gera relatório de projeções estratégicas"""
        report = f"""
# SICOOB - Projeções Estratégicas 2025-2026

## Resumo Executivo
- **Data do Relatório:** {datetime.now().strftime('%d/%m/%Y')}
- **Horizonte de Projeção:** Safra 2025/2026
- **Volume Meta:** R$ 60 bilhões

## Cenários Projetados

### Cenário Otimista
- **Volume:** R$ 65 bilhões (+18%)
- **Inadimplência:** 5.8%
- **Market Share:** 25%

### Cenário Base
- **Volume:** R$ 60 bilhões (+12%)
- **Inadimplência:** 6.5%
- **Market Share:** 23%

### Cenário Pessimista
- **Volume:** R$ 55 bilhões (+3%)
- **Inadimplência:** 7.8%
- **Market Share:** 21%

## Fatores de Risco
- Variações climáticas extremas
- Volatilidade dos preços de commodities
- Mudanças na política monetária
- Intensificação da concorrência

## Estratégias Recomendadas
1. **Hedge Climático:** Expandir seguro paramétrico
2. **Gestão de Taxa:** Produtos com taxa pré-fixada
3. **Diversificação:** Reduzir concentração em commodities
4. **Inovação:** Acelerar transformação digital

## Metas 2025-2026
- Volume: R$ 60 bilhões (+12%)
- Market Share: 24% (+2pp)
- Inadimplência: <6.5%
- ROE: >18%

---
*Projeções Estratégicas - Sistema SICOOB*
        """
        return report
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Relatório de Performance", type="primary"):
            report_content = generate_performance_report(carteira_filtrada, linhas_credito_filtradas, regioes_data_filtradas, regiao_filtro)
            st.success("✅ Relatório de Performance gerado com sucesso!")
            
            # Botões de download
            col_md, col_pdf = st.columns(2)
            with col_md:
                st.download_button(
                    label="📄 Download MD",
                    data=report_content,
                    file_name=f"sicoob_relatorio_performance_{datetime.now().strftime('%Y%m%d')}.md",
                    mime="text/markdown"
                )
            with col_pdf:
                pdf_data = create_pdf_report(report_content, "Relatório de Performance")
                if pdf_data:
                    st.download_button(
                        label="📑 Download PDF",
                        data=pdf_data,
                        file_name=f"sicoob_relatorio_performance_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf"
                    )
    
    with col2:
        if st.button("🔮 Projeções Estratégicas", type="primary"):
            projections_report = generate_strategic_projections_report(volume_atual, inadimplencia_atual)
            st.success("✅ Projeções Estratégicas geradas com sucesso!")
            
            # Botões de download
            col_md, col_pdf = st.columns(2)
            with col_md:
                st.download_button(
                    label="📄 Download MD",
                    data=projections_report,
                    file_name=f"sicoob_projecoes_estrategicas_{datetime.now().strftime('%Y%m%d')}.md",
                    mime="text/markdown"
                )
            with col_pdf:
                pdf_data = create_pdf_report(projections_report, "Projeções Estratégicas")
                if pdf_data:
                    st.download_button(
                        label="📑 Download PDF",
                        data=pdf_data,
                        file_name=f"sicoob_projecoes_estrategicas_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf"
                    )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>🌾 SICOOB - Sistema de Cooperativas de Crédito do Brasil</p>
        <p>Dashboard desenvolvido para análise estratégica da carteira de crédito rural</p>
        <p><em>Dados simulados para fins demonstrativos</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()