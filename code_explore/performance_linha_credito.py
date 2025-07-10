
import pandas as pd
import numpy as np

# Simulação de dados de performance por linha de crédito

np.random.seed(45)

linhas_credito = ["Custeio", "Investimento", "Comercialização", "Pronaf", "Pronamp"]

# Simulação de volume de crédito (em milhões de R$) e taxa de inadimplência (%) por linha de crédito
data = []
for linha in linhas_credito:
    volume = np.random.uniform(100, 1000) # Volume de crédito entre 100 e 1000 milhões
    if linha == "Pronaf":
        inadimplencia = np.random.uniform(0.5, 2.0) # Pronaf geralmente tem menor inadimplência
    elif linha == "Pronamp":
        inadimplencia = np.random.uniform(1.0, 3.0)
    else:
        inadimplencia = np.random.uniform(2.0, 5.0)
    data.append([linha, round(volume, 2), round(inadimplencia, 2)])

df_performance_linha = pd.DataFrame(data, columns=["Linha_Credito", "Volume_Credito_Milhoes_R$", "Taxa_Inadimplencia_%"])

print("Performance por Linha de Crédito (Simulada):")
print(df_performance_linha.to_markdown(index=False))

# Insights sobre performance por linha de crédito
print("\nInsights sobre Performance por Linha de Crédito:")
print("- A análise do volume de crédito por linha revela as modalidades mais procuradas pelos produtores rurais, indicando a demanda por diferentes tipos de financiamento.")
print("- A taxa de inadimplência por linha de crédito é um indicador crucial para avaliar o risco associado a cada modalidade, permitindo ao SICOOB ajustar suas políticas de concessão de crédito.")
print("- Linhas como o Pronaf, voltadas para a agricultura familiar, tendem a apresentar menor inadimplência, enquanto outras modalidades podem demandar maior atenção na gestão de risco.")

# Salvando os dados simulados em CSV
df_performance_linha.to_csv("performance_linha_credito_simulado.csv", index=False)
print("\nDados simulados de performance por linha de crédito salvos em \'performance_linha_credito_simulado.csv\'.")


