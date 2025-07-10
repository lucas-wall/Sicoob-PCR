
import pandas as pd
import numpy as np

# Simulação de dados para identificação de nichos não atendidos

np.random.seed(54)

nichos = [
    "Pequenos Produtores de Orgânicos",
    "Produtores de Frutas Exóticas",
    "Aquicultura Familiar",
    "Produtores Rurais em Áreas Remotas",
    "Jovens Produtores Rurais"
]

# Simulação do tamanho do nicho (número de produtores) e nível de atendimento atual (em %)
data = []
for nicho in nichos:
    tamanho_nicho = np.random.randint(1000, 10000) # Número de produtores
    nivel_atendimento = np.random.uniform(5.0, 40.0) # %
    data.append([nicho, tamanho_nicho, round(nivel_atendimento, 2)])

df_nichos = pd.DataFrame(data, columns=["Nicho", "Tamanho_Nicho_Produtores", "Nivel_Atendimento_Atual_%"])

# Calculando o potencial de mercado não atendido
df_nichos["Potencial_Nao_Atendido_Produtores"] = df_nichos["Tamanho_Nicho_Produtores"] * (100 - df_nichos["Nivel_Atendimento_Atual_%"]) / 100

print("Identificação de Nichos Não Atendidos (Simulada):")
print(df_nichos.sort_values(by="Potencial_Nao_Atendido_Produtores", ascending=False).to_markdown(index=False))

# Insights sobre nichos não atendidos
print("\nInsights sobre Identificação de Nichos Não Atendidos:")
print("- A identificação de nichos não atendidos no mercado de crédito rural representa uma oportunidade estratégica para o SICOOB expandir sua atuação e diversificar sua carteira.")
print("- Nichos como Pequenos Produtores de Orgânicos e Jovens Produtores Rurais, com alto potencial de crescimento e baixo nível de atendimento atual, podem ser prioritários para o SICOOB.")
print("- O SICOOB pode desenvolver produtos e serviços financeiros específicos para atender às necessidades desses nichos, fortalecendo seu papel como cooperativa e contribuindo para o desenvolvimento inclusivo do agronegócio.")

# Salvando os dados simulados em CSV
df_nichos.to_csv("nichos_nao_atendidos_simulado.csv", index=False)
print("\nDados simulados de nichos não atendidos salvos em \"nichos_nao_atendidos_simulado.csv\".")


