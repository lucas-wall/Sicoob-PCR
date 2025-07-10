
import pandas as pd
import numpy as np

# Simulação de dados de concentração geográfica e por cooperativa

np.random.seed(44)

estados = ["MG", "SP", "PR", "GO", "MT", "BA", "RS"]
cooperativas_por_estado = {
    "MG": ["Sicoob Crediminas", "Sicoob Credicom", "Sicoob Credifor"],
    "SP": ["Sicoob Cooplivre", "Sicoob Credicitrus"],
    "PR": ["Sicoob Metropolitano", "Sicoob Unicoob"],
    "GO": ["Sicoob Engecred", "Sicoob UniCentro Norte"],
    "MT": ["Sicoob Primavera", "Sicoob União"],
    "BA": ["Sicoob Central BA", "Sicoob Credisudeste"],
    "RS": ["Sicoob Central SC/RS", "Sicoob Credial"],
}

# Simulação do volume de crédito rural (em milhões de R$) por estado e cooperativa
data = []
for estado in estados:
    for cooperativa in cooperativas_por_estado[estado]:
        volume = np.random.uniform(50, 500) # Volume de crédito entre 50 e 500 milhões
        data.append([estado, cooperativa, round(volume, 2)])

df_concentracao = pd.DataFrame(data, columns=["Estado", "Cooperativa", "Volume_Credito_Milhoes_R$"])

print("Concentração Geográfica e por Cooperativa (Simulada):")
print(df_concentracao.to_markdown(index=False))

# Análise de concentração por estado
df_concentracao_estado = df_concentracao.groupby("Estado")["Volume_Credito_Milhoes_R$"].sum().reset_index()
df_concentracao_estado = df_concentracao_estado.sort_values(by="Volume_Credito_Milhoes_R$", ascending=False)
print("\nConcentração por Estado (Simulada):")
print(df_concentracao_estado.to_markdown(index=False))

# Análise de concentração por cooperativa (top 5)
df_concentracao_cooperativa = df_concentracao.groupby("Cooperativa")["Volume_Credito_Milhoes_R$"].sum().reset_index()
df_concentracao_cooperativa = df_concentracao_cooperativa.sort_values(by="Volume_Credito_Milhoes_R$", ascending=False).head(5)
print("\nTop 5 Cooperativas por Volume de Crédito (Simulada):")
print(df_concentracao_cooperativa.to_markdown(index=False))

# Insights sobre concentração
print("\nInsights sobre Concentração Geográfica e por Cooperativa:")
print("- A análise de concentração geográfica revela as regiões onde o SICOOB possui maior volume de operações de crédito rural, indicando áreas de força e potencial de expansão.")
print("- A distribuição do crédito entre as cooperativas mostra a capilaridade da atuação do SICOOB no agronegócio, com algumas cooperativas se destacando pelo volume de negócios.")
print("- Identificar as cooperativas e regiões com maior e menor concentração de crédito pode auxiliar o SICOOB a otimizar suas estratégias de mercado, direcionando esforços para áreas com maior potencial ou para fortalecer a presença em regiões menos exploradas.")

# Salvando os dados simulados em CSV
df_concentracao.to_csv("concentracao_credito_simulado.csv", index=False)
print("\nDados simulados de concentração salvos em \'concentracao_credito_simulado.csv\'.")


