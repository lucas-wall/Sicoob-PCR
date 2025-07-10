
import pandas as pd
import numpy as np

# Simulação de dados de padrões de inadimplência por região/cultura

np.random.seed(47)

regioes = ["Sudeste", "Sul", "Centro-Oeste", "Nordeste", "Norte"]
culturas = ["Soja", "Milho", "Café", "Cana-de-açúcar", "Algodão"]

data = []
for regiao in regioes:
    for cultura in culturas:
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

        # Ajuste por cultura (algumas culturas podem ter maior risco)
        if cultura == "Soja":
            ajuste_cultura = 0.0
        elif cultura == "Milho":
            ajuste_cultura = 0.2
        elif cultura == "Café":
            ajuste_cultura = 0.5
        elif cultura == "Cana-de-açúcar":
            ajuste_cultura = 0.1
        elif cultura == "Algodão":
            ajuste_cultura = 0.3

        inadimplencia = max(0.5, base_inadimplencia + ajuste_cultura + np.random.uniform(-0.5, 0.5)) # Adiciona ruído
        data.append([regiao, cultura, round(inadimplencia, 2)])

df_inadimplencia_regiao_cultura = pd.DataFrame(data, columns=["Regiao", "Cultura", "Taxa_Inadimplencia_%"])

print("Padrões de Inadimplência por Região e Cultura (Simulada):")
print(df_inadimplencia_regiao_cultura.pivot_table(index="Regiao", columns="Cultura", values="Taxa_Inadimplencia_%").fillna(0).to_markdown())

# Insights sobre padrões de inadimplência
print("\nInsights sobre Padrões de Inadimplência por Região e Cultura:")
print("- A análise dos padrões de inadimplência por região e cultura permite identificar áreas e segmentos com maior ou menor risco de crédito.")
print("- Regiões com maior dependência de culturas específicas ou mais suscetíveis a eventos climáticos podem apresentar taxas de inadimplência mais elevadas.")
print("- O SICOOB pode utilizar essas informações para refinar suas políticas de crédito, ajustar limites de exposição e desenvolver produtos específicos para mitigar riscos em segmentos mais vulneráveis.")

# Salvando os dados simulados em CSV
df_inadimplencia_regiao_cultura.to_csv("inadimplencia_regiao_cultura_simulado.csv", index=False)
print("\nDados simulados de inadimplência por região e cultura salvos em \'inadimplencia_regiao_cultura_simulado.csv\'.")


