
import pandas as pd
import numpy as np

# Simulação de dados para análise de market share por estado

np.random.seed(52)

estados = ["MG", "SP", "PR", "GO", "MT", "BA", "RS"]

data = []
for estado in estados:
    # Market share simulado do SICOOB (em %)
    if estado == "MG":
        sicoob_share = np.random.uniform(15.0, 25.0)
    elif estado == "PR":
        sicoob_share = np.random.uniform(10.0, 20.0)
    elif estado == "MT":
        sicoob_share = np.random.uniform(8.0, 15.0)
    else:
        sicoob_share = np.random.uniform(3.0, 10.0)

    # Market share total do estado (simulado)
    total_market = np.random.uniform(50, 500) # Bilhões de R$

    data.append([estado, round(sicoob_share, 2), round(total_market, 2)])

df_market_share = pd.DataFrame(data, columns=["Estado", "SICOOB_Market_Share_%", "Total_Mercado_Bilhoes_R$"])

print("Análise de Market Share por Estado (Simulada):")
print(df_market_share.sort_values(by="SICOOB_Market_Share_%", ascending=False).to_markdown(index=False))

# Insights sobre market share por estado
print("\nInsights sobre Análise de Market Share por Estado:")
print("- A análise do market share do SICOOB por estado revela sua penetração em diferentes mercados regionais.")
print("- Estados onde o SICOOB possui maior market share indicam uma forte presença e reconhecimento da marca.")
print("- Identificar estados com baixo market share, mas com alto potencial de mercado, pode direcionar estratégias de expansão e investimento para aumentar a participação do SICOOB no crédito rural.")

# Salvando os dados simulados em CSV
df_market_share.to_csv("market_share_estado_simulado.csv", index=False)
print("\nDados simulados de market share por estado salvos em \"market_share_estado_simulado.csv\".")


