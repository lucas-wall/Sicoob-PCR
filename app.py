import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
    
    # Volume da carteira com sazonalidade
    base_volume = 45000  # R$ milhões
    seasonal_factor = np.sin(np.arange(len(dates)) * 2 * np.pi / 12) * 0.15 + 1
    growth_trend = np.linspace(1, 1.25, len(dates))
    volume_carteira = base_volume * seasonal_factor * growth_trend + np.random.normal(0, 1000, len(dates))
    
    carteira_historica = pd.DataFrame({
        'Data': dates,
        'Volume_Milhoes': volume_carteira,
        'Inadimplencia': np.random.normal(6.8, 1.2, len(dates)).clip(3, 12),
        'Numero_Operacoes': (volume_carteira / 150 + np.random.normal(0, 50, len(dates))).astype(int)
    })
    
    # Dados por linha de crédito
    linhas_credito = {
        'Custeio': {'volume': 32000, 'participacao': 60, 'inadimplencia': 6.2},
        'Investimento': {'volume': 12000, 'participacao': 22, 'inadimplencia': 5.8},
        'Comercialização': {'volume': 6500, 'participacao': 12, 'inadimplencia': 7.1},
        'Industrialização': {'volume': 3200, 'participacao': 6, 'inadimplencia': 6.9}
    }
    
    # Dados por região
    regioes_data = {
        'Centro-Oeste': {'volume': 18500, 'cooperativas': 145, 'inadimplencia': 5.9},
        'Sul': {'volume': 16200, 'cooperativas': 178, 'inadimplencia': 6.1},
        'Sudeste': {'volume': 12800, 'cooperativas': 156, 'inadimplencia': 6.8},
        'Nordeste': {'volume': 4200, 'cooperativas': 89, 'inadimplencia': 8.2},
        'Norte': {'volume': 2000, 'cooperativas': 34, 'inadimplencia': 7.5}
    }
    
    # Dados de culturas
    culturas_data = {
        'Soja': {'volume': 22000, 'area_mil_ha': 4200, 'inadimplencia': 5.8},
        'Milho': {'volume': 15000, 'area_mil_ha': 2800, 'inadimplencia': 6.2},
        'Café': {'volume': 8500, 'area_mil_ha': 1900, 'inadimplencia': 6.9},
        'Cana-de-açúcar': {'volume': 4200, 'area_mil_ha': 850, 'inadimplencia': 7.1},
        'Algodão': {'volume': 3800, 'area_mil_ha': 720, 'inadimplencia': 6.5}
    }
    
    return carteira_historica, linhas_credito, regioes_data, culturas_data

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
    
    # Filtrar dados
    mask = (carteira_df['Data'] >= pd.to_datetime(periodo_inicio)) & \
           (carteira_df['Data'] <= pd.to_datetime(periodo_fim))
    carteira_filtrada = carteira_df.loc[mask]
    
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
        fig_linhas = create_linhas_credito_chart(linhas_credito)
        st.plotly_chart(fig_linhas, use_container_width=True)
    
    with col2:
        fig_regional = create_regional_analysis(regioes_data)
        st.plotly_chart(fig_regional, use_container_width=True)
    
    # Insights e Recomendações
    st.markdown("## 💡 Insights e Recomendações")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("🎯 **Oportunidades Identificadas**")
        st.markdown("""
        **Expansão no Nordeste:** Região com menor penetração e alto potencial de crescimento (+150%)
        
        **Digitalização:** 78% dos produtores demandam soluções digitais integradas
        
        **Produtos ESG:** Crescimento de 45% na demanda por crédito sustentável
        
        **Seguro Paramétrico:** Redução de 30% no risco climático com tecnologia
        """)
    
    with col2:
        st.warning("⚠️ **Pontos de Atenção**")
        st.markdown("""
        **Concentração Geográfica:** 65% da carteira concentrada no Centro-Oeste e Sul
        
        **Sazonalidade:** Picos de demanda em março e setembro exigem planejamento
        
        **Risco Climático:** Impacto crescente nas taxas de inadimplência
        
        **Concorrência:** Bancos digitais e fintechs ganhando market share
        """)
    
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
    
    culturas_df = pd.DataFrame(culturas_data).T
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
            cultura_principal = st.selectbox("Cultura Principal", list(culturas_data.keys()), key="cultura_input")
            regiao = st.selectbox("Região", list(regioes_data.keys()), key="regiao_input")
        
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
            risco_cultura = culturas_data[cultura_principal]['inadimplencia']
            risco_regiao = regioes_data[regiao]['inadimplencia']
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
    
    def generate_performance_report(carteira_df, linhas_credito, regioes_data):
        """Gera relatório de performance em markdown"""
        volume_atual = carteira_df['Volume_Milhoes'].iloc[-1]
        inadimplencia_atual = carteira_df['Inadimplencia'].iloc[-1]
        crescimento = ((volume_atual - carteira_df['Volume_Milhoes'].iloc[0]) / carteira_df['Volume_Milhoes'].iloc[0]) * 100
        
        report = f"""
# SICOOB - Relatório de Performance da Carteira Rural

## Resumo Executivo
- **Data do Relatório:** {datetime.now().strftime('%d/%m/%Y')}
- **Período Analisado:** {periodo_inicio.strftime('%d/%m/%Y')} a {periodo_fim.strftime('%d/%m/%Y')}

## Indicadores Principais
- **Volume da Carteira:** R$ {volume_atual:,.0f} milhões
- **Taxa de Inadimplência:** {inadimplencia_atual:.1f}%
- **Crescimento no Período:** {crescimento:+.1f}%
- **Total de Operações:** {carteira_df['Numero_Operacoes'].sum():,}

## Performance por Linha de Crédito
"""
        for linha, dados in linhas_credito.items():
            report += f"- **{linha}:** R$ {dados['volume']:,} Mi ({dados['participacao']}% da carteira)\n"
        
        report += f"""

## Distribuição Regional
"""
        for regiao, dados in regioes_data.items():
            if regiao in regiao_filtro:
                report += f"- **{regiao}:** R$ {dados['volume']:,} Mi ({dados['cooperativas']} cooperativas)\n"
        
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
            report_content = generate_performance_report(carteira_filtrada, linhas_credito, regioes_data)
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