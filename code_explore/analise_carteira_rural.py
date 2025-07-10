
import pandas as pd
import numpy as np

# Simulação de dados históricos de crédito rural do Banco Central (MDCR)
# Em um cenário real, esses dados seriam extraídos da API do BCB ou de arquivos CSV

np.random.seed(42)

# Gerando dados simulados para o período de 2013 a 2024
years = np.arange(2013, 2025)

# Simulação do valor total da carteira de crédito rural (em bilhões de R$)
# Crescimento anual com alguma volatilidade
carteira_rural_base = 100 # Bilhões de R$
crescimento_anual = np.random.uniform(0.08, 0.15, len(years)) # Crescimento entre 8% e 15%
volatilidade = np.random.uniform(0.95, 1.05, len(years)) # Variação de +/- 5%

carteira_rural = [carteira_rural_base * (1 + crescimento_anual[0])]
for i in range(1, len(years)):
    valor_anterior = carteira_rural[i-1]
    novo_valor = valor_anterior * (1 + crescimento_anual[i]) * volatilidade[i]
    carteira_rural.append(novo_valor)

df_carteira = pd.DataFrame({
    'Ano': years,
    'Valor_Carteira_Rural_Bilhoes_R$': [round(v, 2) for v in carteira_rural]
})

print("Evolução Histórica da Carteira de Crédito Rural (Simulada):")
print(df_carteira.to_markdown(index=False))

# Simulação de dados de inadimplência (em %)
inadimplencia_base = 2.0 # %
variacao_anual_inadimplencia = np.random.uniform(-0.5, 0.8, len(years)) # Variação de -0.5 a +0.8 pontos percentuais

inadimplencia = [inadimplencia_base + variacao_anual_inadimplencia[0]]
for i in range(1, len(years)):
    valor_anterior = inadimplencia[i-1]
    novo_valor = max(0.5, valor_anterior + variacao_anual_inadimplencia[i]) # Garante que não seja menor que 0.5%
    inadimplencia.append(novo_valor)

df_inadimplencia = pd.DataFrame({
    'Ano': years,
    'Taxa_Inadimplencia_%': [round(v, 2) for v in inadimplencia]
})

print("\nEvolução Histórica da Taxa de Inadimplência (Simulada):")
print(df_inadimplencia.to_markdown(index=False))

# Exemplo de como os dados seriam usados para gerar insights
print("\nInsights Preliminares (Baseados em Dados Simulados):")
print("- A carteira de crédito rural tem demonstrado um crescimento constante ao longo dos anos, refletindo a expansão do agronegócio brasileiro.")
print("- A taxa de inadimplência, embora com algumas flutuações, mantém-se em patamares controlados, indicando a resiliência do setor.")
print("- A análise detalhada desses dados, em um cenário real, permitiria identificar tendências, períodos de maior risco e oportunidades de crescimento para o SICOOB.")

# Salvando os dados simulados em CSV para futura referência
df_carteira.to_csv('carteira_rural_historico_simulado.csv', index=False)
df_inadimplencia.to_csv('inadimplencia_rural_historico_simulado.csv', index=False)

print("\nDados simulados salvos em 'carteira_rural_historico_simulado.csv' e 'inadimplencia_rural_historico_simulado.csv'.")


