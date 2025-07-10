# Sicoob-PCR: Projeto de Crédito Rural

## 📋 Descrição do Projeto

Este é um aplicativo web moderno desenvolvido com **Streamlit** e **Gradio** para análise estratégica da carteira de crédito rural do SICOOB. O sistema oferece uma interface intuitiva e responsiva para visualização de dados, análise de KPIs e previsão de risco de inadimplência.

📜 &nbsp;Acesse o link público deste projeto:
- [SICOOB - Projeto de Crédito Rural](https://sicoob-pcr-lucaswall.streamlit.app)
<br>
## ✨ Funcionalidades Principais

### 📊 Dashboard Executivo
- **KPIs Principais**: Volume total da carteira, total de operações, ticket médio e taxa de inadimplência
- **Gráficos Interativos**: Evolução temporal, análise por linha de crédito, distribuição regional e por cultura
- **Filtros Avançados**: Por período, linha de crédito, região e cultura
- **Dados Detalhados**: Tabela com informações completas das operações

### 🤖 Sistema de Previsão de Risco
- **Simulador Inteligente**: Análise preditiva de risco de inadimplência
- **Múltiplos Fatores**: Considera valor, taxa de juros, prazo, linha de crédito, cultura e região
- **Classificação Automática**: Baixo risco, risco moderado ou alto risco
- **Recomendações Personalizadas**: Sugestões baseadas no perfil de risco

### 📄 Seção Informativa
- **Documentação Técnica**: Informações sobre tecnologias utilizadas
- **Metodologia**: Explicação do modelo preditivo
- **Objetivos**: Contexto do desenvolvimento para o processo seletivo

## 🛠️ Tecnologias Utilizadas

- **Streamlit**: Framework principal para interface web
- **Gradio**: Interface de machine learning (integração planejada)
- **Plotly**: Visualizações interativas e gráficos
- **Pandas**: Manipulação e análise de dados
- **NumPy**: Computação numérica
- **Python 3.11**: Linguagem de programação

## 🚀 Como Executar

### Pré-requisitos
```bash
# Python 3.11 ou superior
python --version

# Pip para instalação de pacotes
pip --version
```

### Instalação das Dependências
```bash
# Instalar todas as dependências necessárias
pip install streamlit gradio plotly pandas numpy
```

### Executar o Aplicativo
```bash
# Navegar até o diretório do projeto
cd /caminho/para/o/projeto

# Executar o aplicativo Streamlit
streamlit run app.py

# O aplicativo estará disponível em:
# http://localhost:8501
```

### Executar em Servidor (Produção)
```bash
# Para acesso externo (substitua 0.0.0.0 pelo IP do servidor)
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

## 📱 Interface do Usuário

### Design Moderno
- **Cores Institucionais**: Verde (#006341) e Azul (#00A0DF) do SICOOB
- **Bordas Arredondadas**: Design moderno com cantos suavizados
- **Responsividade**: Adaptável para desktop, tablet e mobile
- **Gradientes**: Efeitos visuais elegantes no header e botões

### Navegação Intuitiva
- **Sidebar**: Navegação principal e filtros
- **Seções Organizadas**: Dashboard, Previsão e Sobre o Sistema
- **Feedback Visual**: Hover effects e transições suaves

## 📊 Dados e Modelagem

### Geração de Dados Simulados
O aplicativo utiliza dados simulados que representam operações reais de crédito rural:

```python
# Exemplo de estrutura de dados
{
    'data_operacao': '2024-01-15',
    'valor_operacao': 150000.00,
    'linha_credito': 'Custeio',
    'cultura': 'Soja',
    'regiao': 'Centro-Oeste',
    'cooperativa': 'Cooperativa 1',
    'taxa_juros': 8.5,
    'prazo_meses': 24,
    'status': 'Adimplente'
}
```

### Modelo de Previsão de Risco
O sistema utiliza um modelo baseado em regras que considera:

1. **Valor da Operação**: Operações maiores têm risco ligeiramente maior
2. **Taxa de Juros**: Taxas altas indicam maior risco
3. **Prazo**: Prazos longos aumentam o risco
4. **Linha de Crédito**: Diferentes linhas têm perfis de risco distintos
5. **Cultura**: Algumas culturas são mais voláteis
6. **Região**: Fatores geográficos e climáticos

## 🎨 Customização Visual

### CSS Personalizado
O aplicativo inclui CSS customizado para:
- Gradientes nas cores do SICOOB
- Animações e transições suaves
- Cards com sombras e bordas arredondadas
- Tipografia moderna (Inter font)
- Responsividade completa

### Componentes Visuais
- **Header Gradiente**: Destaque visual com logo e título
- **Cards de KPI**: Métricas com indicadores de variação
- **Gráficos Interativos**: Plotly com tema personalizado
- **Botões Modernos**: Gradientes e efeitos hover

## 📈 KPIs e Métricas

### Indicadores Principais
1. **Volume Total da Carteira**: Soma de todas as operações ativas
2. **Total de Operações**: Quantidade de contratos
3. **Ticket Médio**: Valor médio por operação
4. **Taxa de Inadimplência**: Percentual de operações em atraso

### Análises Disponíveis
- **Evolução Temporal**: Tendência mensal do volume
- **Por Linha de Crédito**: Distribuição entre custeio, investimento, etc.
- **Regional**: Concentração geográfica da carteira
- **Por Cultura**: Performance por tipo de cultivo

## 🔧 Estrutura do Código

```
app.py
├── Configuração do Streamlit
├── CSS Personalizado
├── Funções de Dados
│   ├── generate_sample_data()
│   ├── calculate_kpis()
│   └── create_charts()
├── Interface Principal
│   ├── main_dashboard()
│   ├── create_prediction_interface()
│   └── main()
└── Formatação e Utilitários
```

## 🎯 Contexto do Desenvolvimento

Este aplicativo foi desenvolvido como parte do processo seletivo para a vaga de **Analista em Agronegócio Júnior - Dados** no SICOOB, demonstrando:

- **Competências Técnicas**: Python, análise de dados, visualização
- **Design de Interface**: UX/UI moderno e responsivo
- **Conhecimento do Negócio**: Crédito rural e agronegócio
- **Inovação**: Aplicação de IA para previsão de risco

---

**Desenvolvido com ❤️ para o SICOOB**
*Demonstrando excelência em análise de dados e desenvolvimento de soluções inovadoras para o agronegócio brasileiro.*
