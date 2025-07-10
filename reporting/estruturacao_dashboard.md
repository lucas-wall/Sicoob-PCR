# Estruturação de Páginas e Visualizações para Dashboard de Crédito Rural

## Estrutura Geral do Dashboard

O dashboard de Análise de Crédito Rural do SICOOB será composto por 4 páginas principais, cada uma com foco em um aspecto específico da gestão da carteira de crédito rural. A navegação entre as páginas será feita por meio de botões na parte superior do dashboard.

## 1. Página de Visão Geral da Carteira

### Objetivo
Fornecer uma visão consolidada da carteira de crédito rural, com os principais indicadores de performance e tendências.

### Layout e Visualizações

#### Seção Superior
- **Card 1**: Volume Total da Carteira (R$)
- **Card 2**: Crescimento da Carteira (%)
- **Card 3**: Número de Operações Ativas
- **Card 4**: Ticket Médio (R$)

#### Seção Central
- **Gráfico de Linha**: Evolução mensal do volume da carteira (últimos 24 meses)
- **Gráfico de Barras Empilhadas**: Distribuição do volume por linha de crédito (Custeio, Investimento, Comercialização, Pronaf, Pronamp)

#### Seção Inferior
- **Mapa Geográfico**: Distribuição do volume por estado/região
- **Gráfico de Rosca**: Distribuição por cultura (Soja, Milho, Café, etc.)
- **Tabela**: Top 5 cooperativas por volume

#### Filtros
- Período (Ano, Semestre, Trimestre)
- Região/Estado
- Linha de Crédito
- Cultura

## 2. Página de Análise de Risco

### Objetivo
Monitorar os indicadores de risco da carteira, identificar padrões de inadimplência e avaliar a qualidade do crédito.

### Layout e Visualizações

#### Seção Superior
- **Gauge**: Taxa de Inadimplência (%)
- **Card**: Provisão para Devedores Duvidosos (R$)
- **Card**: Índice de Cobertura (%)
- **Card**: Variação da Inadimplência (p.p.)

#### Seção Central
- **Gráfico de Linha**: Evolução da taxa de inadimplência (últimos 24 meses)
- **Gráfico de Barras**: Inadimplência por linha de crédito
- **Matriz de Calor**: Inadimplência por região e cultura

#### Seção Inferior
- **Gráfico de Dispersão**: Relação entre volume de crédito e taxa de inadimplência por cooperativa
- **Gráfico de Barras**: Inadimplência por tipo de garantia
- **Tabela**: Top 5 regiões com maior inadimplência

#### Filtros
- Período (Ano, Semestre, Trimestre)
- Região/Estado
- Linha de Crédito
- Cultura
- Faixa de Atraso (30, 60, 90+ dias)

## 3. Página de Oportunidades de Mercado

### Objetivo
Identificar oportunidades de crescimento, analisar a participação de mercado e comparar com concorrentes.

### Layout e Visualizações

#### Seção Superior
- **Card**: Market Share Total (%)
- **Card**: Potencial de Crescimento (R$)
- **Card**: Penetração Média (%)
- **Card**: Gap de Mercado (%)

#### Seção Central
- **Gráfico de Barras**: Market Share por estado
- **Gráfico de Linha**: Evolução do Market Share (últimos 24 meses)
- **Gráfico de Barras Horizontais**: Comparativo com concorrentes

#### Seção Inferior
- **Mapa de Calor**: Potencial de crescimento por região
- **Gráfico de Barras Empilhadas**: Penetração por cultura
- **Tabela**: Top 5 nichos com maior potencial

#### Filtros
- Período (Ano, Semestre, Trimestre)
- Região/Estado
- Linha de Crédito
- Cultura

## 4. Página de Simulação de Cenários

### Objetivo
Permitir a simulação de cenários para avaliar o impacto de diferentes variáveis na carteira de crédito rural.

### Layout e Visualizações

#### Seção Superior
- **Controles de Entrada**:
  - Slider para Taxa de Juros
  - Slider para Crescimento da Carteira
  - Slider para Taxa de Inadimplência
  - Dropdown para Eventos Climáticos

#### Seção Central
- **Gráfico de Linha**: Projeção de volume da carteira (próximos 12 meses)
- **Gráfico de Linha**: Projeção de inadimplência (próximos 12 meses)
- **Gráfico de Barras**: Impacto no resultado financeiro

#### Seção Inferior
- **Tabela**: Resumo dos cenários (Otimista, Base, Pessimista)
- **Gráfico de Radar**: Comparativo de indicadores entre cenários
- **Indicadores de Alerta**: Pontos de atenção baseados no cenário selecionado

#### Filtros
- Cenário (Otimista, Base, Pessimista)
- Região/Estado
- Linha de Crédito

## Elementos Comuns a Todas as Páginas

- **Cabeçalho**: Logo do SICOOB, título do dashboard, data de atualização
- **Menu de Navegação**: Botões para alternar entre as páginas
- **Rodapé**: Informações sobre a fonte dos dados, periodicidade de atualização
- **Filtros Globais**: Período, Região/Estado
- **Botão de Exportação**: Para exportar dados ou relatórios em PDF/Excel

## Paleta de Cores e Estilo Visual

- **Cores Primárias**: Verde SICOOB (#006341), Azul SICOOB (#00A0DF)
- **Cores Secundárias**: Tons de verde para categorias, vermelho para alertas
- **Estilo**: Clean, corporativo, com uso de ícones para facilitar a identificação visual
- **Tipografia**: Fonte padrão do SICOOB para manter a identidade visual

## Interatividade

- Drill-down em todos os gráficos para análises mais detalhadas
- Tooltips informativos ao passar o mouse sobre os elementos visuais
- Cross-filtering entre visualizações na mesma página
- Bookmarks para salvar configurações específicas de análise

