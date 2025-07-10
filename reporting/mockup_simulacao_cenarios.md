# Mockup: Página de Simulação de Cenários

## Descrição
Esta página permite aos usuários simular diferentes cenários para avaliar o impacto de variáveis como taxa de juros, crescimento da carteira, inadimplência e eventos climáticos nos resultados da carteira de crédito rural do SICOOB.

## Layout

### Cabeçalho
- Logo do SICOOB (canto superior esquerdo)
- Título: "Dashboard de Crédito Rural - Simulação de Cenários"
- Data de atualização: "Atualizado em: DD/MM/AAAA"
- Menu de navegação com 4 botões: "Visão Geral", "Análise de Risco", "Oportunidades de Mercado", "Simulação de Cenários"

### Seção Superior - Controles de Entrada
Disposição em 4 controles horizontais para ajuste de parâmetros:

**Controle 1: Taxa de Juros**
- Tipo: Slider
- Rótulo: "Taxa de Juros Média (%)"
- Intervalo: 6% a 15%
- Valor padrão: 8,5%
- Incremento: 0,5%

**Controle 2: Crescimento da Carteira**
- Tipo: Slider
- Rótulo: "Crescimento Anual da Carteira (%)"
- Intervalo: 0% a 20%
- Valor padrão: 8%
- Incremento: 1%

**Controle 3: Taxa de Inadimplência**
- Tipo: Slider
- Rótulo: "Taxa de Inadimplência (%)"
- Intervalo: 1% a 10%
- Valor padrão: 2,8%
- Incremento: 0,5%

**Controle 4: Eventos Climáticos**
- Tipo: Dropdown
- Rótulo: "Cenário Climático"
- Opções: "Normal", "Seca Moderada", "Seca Severa", "Excesso de Chuva", "Geada"
- Valor padrão: "Normal"

### Seção Central - Projeções

**Gráfico 1: Projeção de Volume da Carteira**
- Tipo: Gráfico de linha
- Eixo X: Meses (próximos 12 meses)
- Eixo Y: Volume Projetado (R$ Bilhões)
- Linhas múltiplas: Cenário Otimista (verde), Cenário Base (azul), Cenário Pessimista (laranja)
- Linha pontilhada: Cenário atual (baseado nos parâmetros selecionados)

**Gráfico 2: Projeção de Inadimplência**
- Tipo: Gráfico de linha
- Eixo X: Meses (próximos 12 meses)
- Eixo Y: Taxa de Inadimplência Projetada (%)
- Linhas múltiplas: Cenário Otimista (verde), Cenário Base (azul), Cenário Pessimista (laranja)
- Linha pontilhada: Cenário atual (baseado nos parâmetros selecionados)
- Área sombreada: Faixa de tolerância (limite aceitável de inadimplência)

**Gráfico 3: Impacto no Resultado Financeiro**
- Tipo: Gráfico de barras
- Eixo X: Trimestres (próximos 4 trimestres)
- Eixo Y: Resultado Projetado (R$ Milhões)
- Barras agrupadas: Cenário Otimista (verde), Cenário Base (azul), Cenário Pessimista (laranja)
- Linha horizontal: Meta de resultado

### Seção Inferior - Resumo e Comparativos

**Visualização 1: Tabela de Resumo dos Cenários**
- Tipo: Tabela
- Colunas: Indicador, Cenário Otimista, Cenário Base, Cenário Pessimista, Cenário Atual (baseado nos parâmetros)
- Linhas: Volume Final (R$ Bi), Crescimento (%), Inadimplência (%), Resultado (R$ Mi), ROA (%)
- Formatação condicional: Cores de fundo baseadas na comparação com o cenário base

**Visualização 2: Gráfico de Radar - Comparativo de Indicadores**
- Tipo: Gráfico de radar
- Eixos: Volume, Crescimento, Inadimplência, Resultado, ROA
- Áreas: Cenário Otimista (verde), Cenário Base (azul), Cenário Pessimista (laranja), Cenário Atual (linha pontilhada)

**Visualização 3: Indicadores de Alerta**
- Tipo: Cards de alerta
- Conteúdo: Pontos de atenção baseados no cenário selecionado
- Exemplos:
  - "Atenção: Inadimplência projetada acima do limite de tolerância no 3º trimestre"
  - "Oportunidade: Potencial de crescimento 15% acima da meta no segmento de Pronaf"
  - "Risco: Impacto climático pode reduzir o resultado em até 12%"

### Painel de Filtros (Lateral Direita)
- Seletor de Cenário Predefinido: Botões de opção (Otimista, Base, Pessimista)
- Filtro de Região/Estado: Dropdown com seleção múltipla
- Filtro de Linha de Crédito: Checkboxes para seleção múltipla
- Botão "Aplicar Cenário"
- Botão "Resetar Parâmetros"

### Rodapé
- Fonte dos dados: "Fonte: Modelo de Simulação SICOOB"
- Nota: "Os resultados são projeções baseadas em modelos estatísticos e não representam garantia de performance futura"
- Botões de exportação: "Exportar para Excel", "Exportar para PDF", "Salvar Cenário"

## Paleta de Cores
- Cor primária: Verde SICOOB (#006341)
- Cor secundária: Azul SICOOB (#00A0DF)
- Cenário Otimista: Verde (#28A745)
- Cenário Base: Azul (#0066CC)
- Cenário Pessimista: Laranja (#FD7E14)
- Alertas: Vermelho (#DC3545)
- Cor de fundo: Branco (#FFFFFF) para o dashboard
- Cor de texto: Cinza escuro (#333333) para textos e títulos

## Interatividade
- Atualização em tempo real: Todos os gráficos e visualizações se atualizam automaticamente ao ajustar os controles
- Tooltips detalhados ao passar o mouse sobre os elementos visuais
- Possibilidade de salvar cenários personalizados para análise posterior
- Botão para exportar relatório completo da simulação

## Referências Visuais
Baseado nas melhores práticas de design de dashboards de simulação financeira, com inspiração nos seguintes elementos:
- Controles intuitivos para ajuste de parâmetros
- Visualização comparativa de múltiplos cenários
- Gráfico de radar para análise multidimensional
- Sistema de alertas para identificação rápida de riscos e oportunidades

