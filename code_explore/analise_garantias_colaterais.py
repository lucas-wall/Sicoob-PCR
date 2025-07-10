
import pandas as pd
import numpy as np

# Simulação de dados para análise de garantias e colaterais

np.random.seed(49)

tipos_garantia = ["Fiança", "Penhor Agrícola", "Hipoteca Rural", "Alienação Fiduciária", "Sem Garantia"]

# Simulação do volume de crédito (em milhões de R$) e taxa de inadimplência (%) por tipo de garantia
data = []
for garantia in tipos_garantia:
    volume = np.random.uniform(100, 800) # Volume de crédito entre 100 e 800 milhões
    if garantia == "Sem Garantia":
        inadimplencia = np.random.uniform(8.0, 15.0) # Maior inadimplência para sem garantia
    elif garantia == "Fiança":
        inadimplencia = np.random.uniform(3.0, 6.0)
    else:
        inadimplencia = np.random.uniform(1.0, 4.0)
    data.append([garantia, round(volume, 2), round(inadimplencia, 2)])

df_garantias = pd.DataFrame(data, columns=["Tipo_Garantia", "Volume_Credito_Milhoes_R$", "Taxa_Inadimplencia_%"])

print("Análise de Garantias e Colaterais (Simulada):")
print(df_garantias.sort_values(by="Taxa_Inadimplencia_%", ascending=False).to_markdown(index=False))

# Insights sobre garantias e colaterais
print("\nInsights sobre Análise de Garantias e Colaterais:")
print("- A análise dos tipos de garantia e sua relação com a inadimplência é crucial para a gestão de risco do crédito rural.")
print("- Empréstimos sem garantia tendem a apresentar taxas de inadimplência significativamente mais altas, reforçando a importância da avaliação de colaterais.")
print("- O SICOOB pode utilizar essas informações para definir políticas de exigência de garantias mais adequadas, mitigar riscos e otimizar a composição de sua carteira de crédito rural.")

# Salvando os dados simulados em CSV
df_garantias.to_csv("analise_garantias_colaterais_simulado.csv", index=False)
print("\nDados simulados de garantias e colaterais salvos em \'analise_garantias_colaterais_simulado.csv\'.")


