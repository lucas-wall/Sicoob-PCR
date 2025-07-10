
import pandas as pd
import numpy as np

# Simulação de dados para oportunidades de crescimento por região

np.random.seed(51)

regioes = ["Sudeste", "Sul", "Centro-Oeste", "Nordeste", "Norte"]

data = []
for regiao in regioes:
    # Potencial de crescimento (em %)
    if regiao == "Sudeste":
        potencial_crescimento = np.random.uniform(5.0, 10.0)
    elif regiao == "Sul":
        potencial_crescimento = np.random.uniform(7.0, 12.0)
    elif regiao == "Centro-Oeste":
        potencial_crescimento = np.random.uniform(10.0, 18.0) # Maior potencial
    elif regiao == "Nordeste":
        potencial_crescimento = np.random.uniform(8.0, 15.0)
    elif regiao == "Norte":
        potencial_crescimento = np.random.uniform(6.0, 11.0)

    # Volume atual de crédito (em bilhões de R$)
    volume_atual = np.random.uniform(5, 50)

    data.append([regiao, round(volume_atual, 2), round(potencial_crescimento, 2)])

df_oportunidades = pd.DataFrame(data, columns=["Regiao", "Volume_Credito_Atual_Bilhoes_R$", "Potencial_Crescimento_%"])

print("Oportunidades de Crescimento por Região (Simulada):")
print(df_oportunidades.sort_values(by="Potencial_Crescimento_%", ascending=False).to_markdown(index=False))

# Insights sobre oportunidades de crescimento
print("\nInsights sobre Oportunidades de Crescimento por Região:")
print("- A análise do potencial de crescimento por região permite ao SICOOB identificar mercados com maior espaço para expansão de suas operações de crédito rural.")
print("- Regiões como o Centro-Oeste, com grande vocação agrícola, tendem a apresentar maior potencial de crescimento, demandando maior atenção e investimento.")
print("- O SICOOB pode direcionar seus esforços de marketing e expansão para as regiões com maior potencial, desenvolvendo produtos e serviços específicos para atender às necessidades desses mercados.")

# Salvando os dados simulados em CSV
df_oportunidades.to_csv("oportunidades_crescimento_regiao_simulado.csv", index=False)
print("\nDados simulados de oportunidades de crescimento por região salvos em \'oportunidades_crescimento_regiao_simulado.csv\'.")


