
import pandas as pd
import numpy as np

# Simulação de dados para sugestão de limites de crédito

np.random.seed(59)

num_clientes = 500

# Geração de dados simulados de clientes
renda_anual = np.random.normal(loc=100000, scale=40000, size=num_clientes) # Renda anual em R$
divida_atual = np.random.normal(loc=15000, scale=8000, size=num_clientes) # Dívida atual
historico_pagamento_score = np.random.uniform(0.3, 0.9, size=num_clientes) # Score de 0.3 (ruim) a 0.9 (bom)

# Simulação de risco de inadimplência (baseado no score, renda e dívida)
prob_inadimplencia = 1 - (historico_pagamento_score * (renda_anual / 200000) / (divida_atual / 20000)) # Simplificado
prob_inadimplencia = np.clip(prob_inadimplencia, 0.01, 0.5) # Limita a probabilidade entre 1% e 50%

df_clientes_limite = pd.DataFrame({
    "ID_Cliente": range(1, num_clientes + 1),
    "Renda_Anual": [round(max(20000, r), 2) for r in renda_anual],
    "Divida_Atual": [round(max(0, d), 2) for d in divida_atual],
    "Historico_Pagamento_Score": [round(s, 2) for s in historico_pagamento_score],
    "Prob_Inadimplencia": [round(p, 4) for p in prob_inadimplencia]
})

# Lógica de sugestão de limite de crédito
# Limite base = 30% da renda anual
# Ajuste pelo score de pagamento e probabilidade de inadimplência

df_clientes_limite["Limite_Sugerido"] = df_clientes_limite.apply(lambda row:
    round(0.3 * row["Renda_Anual"] * row["Historico_Pagamento_Score"] * (1 - row["Prob_Inadimplencia"]), 2)
, axis=1)

# Garantir que o limite não seja negativo e tenha um mínimo
df_clientes_limite["Limite_Sugerido"] = df_clientes_limite["Limite_Sugerido"].apply(lambda x: max(1000, x))

print("Sugestão de Limites de Crédito (Simulada - Amostra):")
print(df_clientes_limite.head().to_markdown(index=False))

# Insights sobre sugestão de limites de crédito
print("\nInsights sobre Sugestão de Limites de Crédito:")
print("- A sugestão de limites de crédito baseada em fatores como renda, dívida atual, histórico de pagamento e probabilidade de inadimplência permite ao SICOOB oferecer crédito de forma mais responsável e personalizada.")
print("- Clientes com melhor perfil de risco podem receber limites mais altos, enquanto aqueles com maior risco podem ter limites mais conservadores.")
print("- Essa abordagem otimiza a alocação de capital, minimiza o risco de inadimplência e maximiza a rentabilidade da carteira de crédito rural do SICOOB.")

# Salvando os dados simulados em CSV
df_clientes_limite.to_csv("sugestao_limites_credito_simulado.csv", index=False)
print("\nDados simulados de sugestão de limites de crédito salvos em \"sugestao_limites_credito_simulado.csv\".")


