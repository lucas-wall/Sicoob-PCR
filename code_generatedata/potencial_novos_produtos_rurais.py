
import pandas as pd
import numpy as np

# Simulação de dados para potencial de novos produtos rurais

np.random.seed(53)

novos_produtos = [
    "Crédito para Agricultura Orgânica",
    "Financiamento para Energias Renováveis (Fazendas)",
    "Crédito para Inovação Tecnológica no Campo",
    "Seguro Agrícola Personalizado",
    "Crédito para Pequenos Produtores (Microcrédito Rural)"
]

# Simulação do potencial de mercado (em bilhões de R$) e taxa de adoção (%) para novos produtos
data = []
for produto in novos_produtos:
    potencial_mercado = np.random.uniform(0.5, 5.0) # Bilhões de R$
    taxa_adocao = np.random.uniform(5.0, 30.0) # %
    data.append([produto, round(potencial_mercado, 2), round(taxa_adocao, 2)])

df_novos_produtos = pd.DataFrame(data, columns=["Novo_Produto", "Potencial_Mercado_Bilhoes_R$", "Taxa_Adocao_%"])

print("Potencial de Novos Produtos Rurais (Simulada):")
print(df_novos_produtos.sort_values(by="Potencial_Mercado_Bilhoes_R$", ascending=False).to_markdown(index=False))

# Insights sobre potencial de novos produtos
print("\nInsights sobre Potencial de Novos Produtos Rurais:")
print("- A identificação do potencial de novos produtos rurais permite ao SICOOB diversificar sua oferta e atender às demandas emergentes do agronegócio.")
print("- Produtos como crédito para agricultura orgânica e energias renováveis refletem tendências de sustentabilidade e inovação no campo.")
print("- O SICOOB pode investir no desenvolvimento e na promoção desses novos produtos, posicionando-se como um parceiro estratégico para produtores que buscam modernização e práticas mais sustentáveis.")

# Salvando os dados simulados em CSV
df_novos_produtos.to_csv("potencial_novos_produtos_rurais_simulado.csv", index=False)
print("\nDados simulados de potencial de novos produtos rurais salvos em \"potencial_novos_produtos_rurais_simulado.csv\".")


