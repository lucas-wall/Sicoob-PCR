# Mockup: Página de Visão Geral da Carteira

## Descrição
Esta página fornece uma visão consolidada da carteira de crédito rural do SICOOB, apresentando os principais indicadores de performance, distribuição geográfica, por linha de crédito e por cultura.

## Layout

### Cabeçalho
- Logo do SICOOB (canto superior esquerdo)
- Título: "Dashboard de Crédito Rural - Visão Geral da Carteira"
- Data de atualização: "Atualizado em: DD/MM/AAAA"
- Menu de navegação com 4 botões: "Visão Geral", "Análise de Risco", "Oportunidades de Mercado", "Simulação de Cenários"

### Seção Superior - Cards de KPIs
Disposição em 4 cards horizontais com os principais indicadores:

**Card 1: Volume Total da Carteira**
- Valor: R$ 12,5 Bilhões
- Variação: +8,2% vs. ano anterior (seta verde para cima)
- Ícone: gráfico de barras

**Card 2: Número de Operações**
- Valor: 45.782
- Variação: +5,7% vs. ano anterior (seta verde para cima)
- Ícone: documento/contrato

**Card 3: Ticket Médio**
- Valor: R$ 273.000
- Variação: +2,4% vs. ano anterior (seta verde para cima)
- Ícone: calculadora

**Card 4: Taxa de Inadimplência**
- Valor: 2,8%
- Variação: -0,5 p.p. vs. ano anterior (seta verde para baixo)
- Ícone: alerta/sino

### Seção Central - Gráficos Principais

**Gráfico 1: Evolução do Volume da Carteira (últimos 24 meses)**
- Tipo: Gráfico de linha
- Eixo X: Meses (Jan/2023 a Dez/2024)
- Eixo Y: Volume em Bilhões de R$
- Linha de tendência: crescente
- Marcação de sazonalidade (picos em períodos de plantio)

**Gráfico 2: Distribuição por Linha de Crédito**
- Tipo: Gráfico de barras empilhadas
- Eixo X: Anos (2023, 2024)
- Eixo Y: Volume em Bilhões de R$
- Segmentação por cores:
  - Custeio: Verde escuro
  - Investimento: Verde claro
  - Comercialização: Azul
  - Pronaf: Laranja
  - Pronamp: Amarelo

### Seção Inferior - Distribuição Geográfica e por Cultura

**Visualização 1: Mapa do Brasil**
- Tipo: Mapa geográfico com gradiente de cores
- Intensidade de cor por volume de crédito
- Tooltip ao passar o mouse: Volume, Número de operações, Inadimplência

**Visualização 2: Distribuição por Cultura**
- Tipo: Gráfico de rosca
- Segmentação por cores para cada cultura:
  - Soja: Verde
  - Milho: Amarelo
  - Café: Marrom
  - Cana-de-açúcar: Verde claro
  - Algodão: Branco
  - Outros: Cinza

**Visualização 3: Top 5 Cooperativas**
- Tipo: Tabela
- Colunas: Posição, Nome da Cooperativa, Volume (R$), Participação (%), Variação (%)
- Ordenação: Por volume, decrescente

### Painel de Filtros (Lateral Direita)
- Filtro de Período: Dropdown com opções (Último ano, Último semestre, Último trimestre, Personalizado)
- Filtro de Região/Estado: Dropdown com seleção múltipla
- Filtro de Linha de Crédito: Checkboxes para seleção múltipla
- Filtro de Cultura: Checkboxes para seleção múltipla
- Botão "Limpar Filtros"

### Rodapé
- Fonte dos dados: "Fonte: Sistema Interno SICOOB"
- Periodicidade: "Atualização: Mensal"
- Botões de exportação: "Exportar para Excel", "Exportar para PDF"

## Paleta de Cores
- Cor primária: Verde SICOOB (#006341)
- Cor secundária: Azul SICOOB (#00A0DF)
- Cores de apoio: Tons de verde para categorias
- Cor de alerta: Vermelho (#E63946) para indicadores negativos
- Cor de fundo: Branco (#FFFFFF) para o dashboard
- Cor de texto: Cinza escuro (#333333) para textos e títulos

## Interatividade
- Drill-down no mapa: Ao clicar em um estado, exibe detalhamento por cooperativas
- Cross-filtering: Ao selecionar uma linha de crédito, todos os gráficos são filtrados
- Tooltips informativos ao passar o mouse sobre os elementos visuais
- Botões para alternar entre visualização percentual e absoluta nos gráficos

## Referências Visuais
Baseado nas melhores práticas de design de dashboards financeiros do Power BI, com inspiração nos seguintes elementos:
- Layout limpo e organizado com cards de KPIs destacados
- Uso de cores institucionais do SICOOB
- Visualizações complementares que permitem análise de diferentes perspectivas
- Filtros intuitivos para facilitar a exploração dos dados

