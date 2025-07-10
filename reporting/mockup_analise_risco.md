# Mockup: Página de Análise de Risco

## Descrição
Esta página apresenta uma análise detalhada dos indicadores de risco da carteira de crédito rural do SICOOB, permitindo identificar padrões de inadimplência, avaliar a qualidade do crédito e monitorar a exposição ao risco por diferentes segmentos.

## Layout

### Cabeçalho
- Logo do SICOOB (canto superior esquerdo)
- Título: "Dashboard de Crédito Rural - Análise de Risco"
- Data de atualização: "Atualizado em: DD/MM/AAAA"
- Menu de navegação com 4 botões: "Visão Geral", "Análise de Risco", "Oportunidades de Mercado", "Simulação de Cenários"

### Seção Superior - Indicadores de Risco
Disposição em 4 visualizações horizontais:

**Visualização 1: Taxa de Inadimplência**
- Tipo: Gauge (velocímetro)
- Valor atual: 2,8%
- Faixas de risco:
  - Verde: 0% a 3% (Baixo risco)
  - Amarelo: 3% a 5% (Médio risco)
  - Vermelho: Acima de 5% (Alto risco)
- Meta: 2,5% (marcada com linha pontilhada)

**Visualização 2: Provisão para Devedores Duvidosos (PDD)**
- Tipo: Card numérico
- Valor: R$ 350 Milhões
- Variação: +5,2% vs. ano anterior (seta vermelha para cima)
- Ícone: escudo/proteção

**Visualização 3: Índice de Cobertura**
- Tipo: Card numérico
- Valor: 125%
- Variação: +3,5 p.p. vs. ano anterior (seta verde para cima)
- Ícone: guarda-chuva/proteção

**Visualização 4: Variação da Inadimplência**
- Tipo: Sparkline (mini gráfico de linha)
- Tendência dos últimos 12 meses
- Valor atual: -0,5 p.p. (seta verde para baixo)
- Ícone: gráfico/tendência

### Seção Central - Análise Temporal e Segmentada

**Gráfico 1: Evolução da Taxa de Inadimplência**
- Tipo: Gráfico de linha
- Eixo X: Meses (últimos 24 meses)
- Eixo Y: Taxa de Inadimplência (%)
- Linha de referência: Meta de inadimplência (2,5%)
- Linha de tendência: decrescente

**Gráfico 2: Inadimplência por Linha de Crédito**
- Tipo: Gráfico de barras horizontais
- Eixo X: Taxa de Inadimplência (%)
- Eixo Y: Linhas de Crédito (Custeio, Investimento, Comercialização, Pronaf, Pronamp)
- Cores: Gradiente de verde (menor inadimplência) a vermelho (maior inadimplência)
- Linha de referência: Média geral de inadimplência (2,8%)

**Gráfico 3: Matriz de Calor - Inadimplência por Região e Cultura**
- Tipo: Mapa de calor (heatmap)
- Eixo X: Culturas (Soja, Milho, Café, Cana-de-açúcar, Algodão)
- Eixo Y: Regiões (Norte, Nordeste, Centro-Oeste, Sudeste, Sul)
- Intensidade de cor: Verde (baixa inadimplência) a Vermelho (alta inadimplência)
- Valores numéricos dentro de cada célula

### Seção Inferior - Análise Detalhada

**Visualização 1: Relação Volume vs. Inadimplência por Cooperativa**
- Tipo: Gráfico de dispersão (scatter plot)
- Eixo X: Volume de Crédito (R$ Milhões)
- Eixo Y: Taxa de Inadimplência (%)
- Tamanho dos pontos: Número de operações
- Cores dos pontos: Por região
- Tooltip: Nome da cooperativa, volume, inadimplência, número de operações

**Visualização 2: Inadimplência por Tipo de Garantia**
- Tipo: Gráfico de barras
- Eixo X: Tipos de Garantia (Fiança, Penhor Agrícola, Hipoteca Rural, Alienação Fiduciária, Sem Garantia)
- Eixo Y: Taxa de Inadimplência (%)
- Cores: Gradiente de verde (menor inadimplência) a vermelho (maior inadimplência)

**Visualização 3: Top 5 Regiões com Maior Inadimplência**
- Tipo: Tabela
- Colunas: Posição, Região, Volume (R$), Taxa de Inadimplência (%), Variação (p.p.)
- Ordenação: Por taxa de inadimplência, decrescente
- Formatação condicional: Cores de fundo baseadas na taxa de inadimplência

### Painel de Filtros (Lateral Direita)
- Filtro de Período: Dropdown com opções (Último ano, Último semestre, Último trimestre, Personalizado)
- Filtro de Região/Estado: Dropdown com seleção múltipla
- Filtro de Linha de Crédito: Checkboxes para seleção múltipla
- Filtro de Cultura: Checkboxes para seleção múltipla
- Filtro de Faixa de Atraso: Botões de opção (30 dias, 60 dias, 90+ dias)
- Botão "Limpar Filtros"

### Rodapé
- Fonte dos dados: "Fonte: Sistema Interno SICOOB"
- Periodicidade: "Atualização: Mensal"
- Botões de exportação: "Exportar para Excel", "Exportar para PDF"

## Paleta de Cores
- Cor primária: Verde SICOOB (#006341)
- Cor secundária: Azul SICOOB (#00A0DF)
- Gradiente de risco: Verde (#28A745) para baixo risco, Amarelo (#FFC107) para médio risco, Vermelho (#DC3545) para alto risco
- Cor de fundo: Branco (#FFFFFF) para o dashboard
- Cor de texto: Cinza escuro (#333333) para textos e títulos

## Interatividade
- Drill-down na matriz de calor: Ao clicar em uma célula, exibe detalhamento por cooperativas
- Cross-filtering: Ao selecionar um tipo de garantia, todos os gráficos são filtrados
- Tooltips informativos ao passar o mouse sobre os elementos visuais
- Botões para alternar entre visualização percentual e absoluta nos gráficos

## Referências Visuais
Baseado nas melhores práticas de design de dashboards de análise de risco, com inspiração nos seguintes elementos:
- Uso de gauge para indicadores de risco com faixas de alerta
- Matriz de calor para identificação rápida de áreas problemáticas
- Gráfico de dispersão para análise de correlação entre volume e inadimplência
- Cores intuitivas que representam níveis de risco (verde, amarelo, vermelho)

