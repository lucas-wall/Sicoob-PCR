
import pandas as pd
import numpy as np

# Simulação de dados para comparação com concorrentes

np.random.seed(46)

concorrentes = ["Banco do Brasil", "Bradesco", "Santander", "Caixa Econômica Federal"]

# Simulação do volume de crédito rural (em bilhões de R$) e taxa de inadimplência (%) para concorrentes
data = []
for concorrente in concorrentes:
    volume = np.random.uniform(50, 500) # Volume de crédito entre 50 e 500 bilhões
    inadimplencia = np.random.uniform(2.5, 6.0) # Taxa de inadimplência entre 2.5% e 6.0%
    data.append([concorrente, round(volume, 2), round(inadimplencia, 2)])

df_concorrentes = pd.DataFrame(data, columns=["Instituicao", "Volume_Credito_Rural_Bilhoes_R$", "Taxa_Inadimplencia_%"])

# Adicionando dados simulados do SICOOB para comparação (usando um valor médio da simulação anterior)
sicoob_volume = 250 # Bilhões de R$
sicoob_inadimplencia = 2.5 # %

df_sicoob = pd.DataFrame({
    "Instituicao": ["SICOOB"],
    "Volume_Credito_Rural_Bilhoes_R$": [sicoob_volume],
    "Taxa_Inadimplencia_%": [sicoob_inadimplencia]
})

df_comparacao = pd.concat([df_sicoob, df_concorrentes], ignore_index=True)

print("Comparação com Concorrentes (Simulada):")
print(df_comparacao.sort_values(by="Volume_Credito_Rural_Bilhoes_R$", ascending=False).to_markdown(index=False))

# Insights sobre comparação com concorrentes
print("\nInsights sobre Comparação com Concorrentes:")
print("- A comparação do volume de crédito rural do SICOOB com seus principais concorrentes permite avaliar sua posição no mercado e identificar oportunidades de crescimento.")
print("- A taxa de inadimplência, quando comparada com a dos concorrentes, pode indicar a eficiência das políticas de crédito e gestão de risco do SICOOB.")
print("- Em um cenário real, essa análise detalhada ajudaria o SICOOB a identificar as melhores práticas do mercado, ajustar suas estratégias de precificação e oferta de produtos, e fortalecer sua competitividade no segmento de crédito rural.")

# Salvando os dados simulados em CSV
df_comparacao.to_csv("comparacao_concorrentes_simulado.csv", index=False)
print("\nDados simulados de comparação com concorrentes salvos em \'comparacao_concorrentes_simulado.csv\'.")


