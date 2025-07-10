
import pandas as pd
import numpy as np

# Simulação de dados de impacto de fatores climáticos nos pagamentos

np.random.seed(48)

regioes = ["Sudeste", "Sul", "Centro-Oeste", "Nordeste", "Norte"]
eventos_climaticos = ["Seca", "Excesso de Chuva", "Geada", "Normal"]

data = []
for regiao in regioes:
    for evento in eventos_climaticos:
        # Inadimplência base por região
        if regiao == "Sudeste":
            base_inadimplencia = 2.0
        elif regiao == "Sul":
            base_inadimplencia = 1.8
        elif regiao == "Centro-Oeste":
            base_inadimplencia = 2.5
        elif regiao == "Nordeste":
            base_inadimplencia = 3.5
        elif regiao == "Norte":
            base_inadimplencia = 3.0

        # Ajuste por evento climático
        if evento == "Seca":
            ajuste_evento = 1.5
        elif evento == "Excesso de Chuva":
            ajuste_evento = 1.0
        elif evento == "Geada":
            ajuste_evento = 0.8
        elif evento == "Normal":
            ajuste_evento = 0.0

        inadimplencia = max(0.5, base_inadimplencia + ajuste_evento + np.random.uniform(-0.5, 0.5)) # Adiciona ruído
        data.append([regiao, evento, round(inadimplencia, 2)])

df_impacto_climatico = pd.DataFrame(data, columns=["Regiao", "Evento_Climatico", "Taxa_Inadimplencia_%"])

print("Impacto de Fatores Climáticos nos Pagamentos (Simulada):")
print(df_impacto_climatico.pivot_table(index="Regiao", columns="Evento_Climatico", values="Taxa_Inadimplencia_%").fillna(0).to_markdown())

# Insights sobre impacto climático
print("\nInsights sobre Impacto de Fatores Climáticos nos Pagamentos:")
print("- Eventos climáticos adversos, como secas e excesso de chuva, têm um impacto direto e significativo na taxa de inadimplência do crédito rural.")
print("- Regiões mais suscetíveis a determinados eventos climáticos podem apresentar maior risco de inadimplência em períodos de adversidade.")
print("- O SICOOB pode utilizar essas informações para aprimorar seus modelos de risco, desenvolver produtos de seguro rural e oferecer suporte aos produtores em momentos de crise climática, minimizando o impacto na carteira de crédito.")

# Salvando os dados simulados em CSV
df_impacto_climatico.to_csv("impacto_climatico_pagamentos_simulado.csv", index=False)
print("\nDados simulados de impacto climático salvos em \'impacto_climatico_pagamentos_simulado.csv\'.")


