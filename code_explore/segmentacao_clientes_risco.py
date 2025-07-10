
import pandas as pd
import numpy as np

# Simulação de dados para segmentação de clientes por risco

np.random.seed(50)

num_clientes = 1000

# Geração de dados simulados para características de clientes
renda_anual = np.random.normal(loc=100000, scale=50000, size=num_clientes) # Renda anual em R$
area_propriedade = np.random.normal(loc=50, scale=20, size=num_clientes) # Área da propriedade em hectares
historico_pagamento = np.random.uniform(0, 1, size=num_clientes) # 0 = ruim, 1 = bom
idade_produtor = np.random.randint(25, 70, size=num_clientes)

# Classificação de risco baseada em algumas regras simples
def classificar_risco(row):
    risco = "Baixo"
    if row["Historico_Pagamento"] < 0.4:
        risco = "Alto"
    elif row["Historico_Pagamento"] < 0.7:
        risco = "Médio"

    if row["Renda_Anual_R$"] < 50000 and risco != "Alto": # Corrigido o nome da coluna
        risco = "Médio"
    if row["Area_Propriedade_Hectares"] < 10 and risco == "Baixo":
        risco = "Médio"
    if row["Idade_Produtor"] > 60 and risco == "Baixo":
        risco = "Médio"

    return risco

df_clientes = pd.DataFrame({
    "ID_Cliente": range(1, num_clientes + 1),
    "Renda_Anual_R$": [round(max(10000, r), 2) for r in renda_anual], # Renda mínima de 10k
    "Area_Propriedade_Hectares": [round(max(1, a), 2) for a in area_propriedade], # Área mínima de 1
    "Historico_Pagamento": [round(h, 2) for h in historico_pagamento],
    "Idade_Produtor": idade_produtor
})

df_clientes["Segmento_Risco"] = df_clientes.apply(classificar_risco, axis=1)

print("Segmentação de Clientes por Risco (Simulada - Amostra):")
print(df_clientes.head().to_markdown(index=False))

# Contagem por segmento de risco
print("\nContagem de Clientes por Segmento de Risco:")
print(df_clientes["Segmento_Risco"].value_counts().to_markdown())

# Insights sobre segmentação de clientes
print("\nInsights sobre Segmentação de Clientes por Risco:")
print("- A segmentação de clientes por risco permite ao SICOOB categorizar seus cooperados com base em fatores financeiros, históricos e demográficos.")
print("- Essa categorização é fundamental para a tomada de decisões estratégicas, como a definição de limites de crédito, condições de empréstimo e estratégias de recuperação de crédito.")
print("- Clientes de baixo risco podem ser elegíveis a condições mais favoráveis, enquanto clientes de alto risco podem demandar acompanhamento mais próximo e garantias adicionais.")

# Salvando os dados simulados em CSV
df_clientes.to_csv("segmentacao_clientes_risco_simulado.csv", index=False)
print("\nDados simulados de segmentação de clientes por risco salvos em \"segmentacao_clientes_risco_simulado.csv\".")


