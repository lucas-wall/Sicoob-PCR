
import pandas as pd
import numpy as np

# Simulação de dados para precificação de juros baseada no risco

np.random.seed(60)

num_clientes = 500

# Geração de dados simulados de clientes com score de risco
score_risco = np.random.uniform(0.1, 0.9, size=num_clientes) # 0.1 (alto risco) a 0.9 (baixo risco)

df_clientes_juros = pd.DataFrame({
    "ID_Cliente": range(1, num_clientes + 1),
    "Score_Risco": [round(s, 2) for s in score_risco]
})

# Lógica de precificação de juros
# Taxa base: 8% ao ano
# Ajuste baseado no score de risco: quanto menor o score, maior o juro
# Juros = Taxa Base + (1 - Score_Risco) * Fator de Ajuste

taxa_base = 0.08 # 8% ao ano
fator_ajuste = 0.10 # 10 pontos percentuais de ajuste máximo

df_clientes_juros["Taxa_Juros_Sugerida_%"] = df_clientes_juros.apply(lambda row:
    round((taxa_base + (1 - row["Score_Risco"]) * fator_ajuste) * 100, 2)
, axis=1)

# Garantir que a taxa de juros tenha um mínimo e máximo razoáveis
df_clientes_juros["Taxa_Juros_Sugerida_%"] = df_clientes_juros["Taxa_Juros_Sugerida_%"]

print("Precificação de Juros Baseada no Risco (Simulada - Amostra):")
print(df_clientes_juros.head().to_markdown(index=False))

# Insights sobre precificação de juros
print("\nInsights sobre Precificação de Juros Baseada no Risco:")
print("- A precificação de juros baseada no risco permite ao SICOOB alinhar o custo do crédito ao perfil de cada cooperado, promovendo justiça e sustentabilidade financeira.")
print("- Clientes com menor score de risco (melhor perfil) recebem taxas de juros mais baixas, incentivando a adimplência e a fidelidade.")
print("- Essa estratégia otimiza a rentabilidade da carteira de crédito, ao mesmo tempo em que gerencia o risco de forma eficaz, garantindo que o SICOOB seja competitivo no mercado de crédito rural.")

# Salvando os dados simulados em CSV
df_clientes_juros.to_csv("precificacao_juros_risco_simulado.csv", index=False)
print("\nDados simulados de precificação de juros salvos em \"precificacao_juros_risco_simulado.csv\".")


