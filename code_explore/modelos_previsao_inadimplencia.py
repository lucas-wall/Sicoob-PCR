
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

# Simulação de dados para modelos de previsão de inadimplência

np.random.seed(58) # Alterando a seed novamente

num_clientes = 1000

# Geração de dados simulados (incluindo fatores climáticos e econômicos)
renda = np.random.normal(loc=100000, scale=30000, size=num_clientes)
divida_atual = np.random.normal(loc=20000, scale=10000, size=num_clientes)
area_plantada = np.random.normal(loc=50, scale=20, size=num_clientes)
preco_commodity = np.random.normal(loc=100, scale=10, size=num_clientes)
chuva_anual = np.random.normal(loc=1500, scale=300, size=num_clientes)

# Criando uma variável alvo mais balanceada
# Gerar uma proporção desejada de inadimplentes (e.g., 20%)
num_inadimplentes_desejado = int(num_clientes * 0.20)
num_adimplentes_desejado = num_clientes - num_inadimplentes_desejado

inadimplencia = np.zeros(num_clientes, dtype=int)
inadimplencia[:num_inadimplentes_desejado] = 1
np.random.shuffle(inadimplencia) # Embaralhar para misturar as classes

df_inadimplencia = pd.DataFrame({
    "Renda": renda,
    "Divida_Atual": divida_atual,
    "Area_Plantada": area_plantada,
    "Preco_Commodity": preco_commodity,
    "Chuva_Anual": chuva_anual,
    "Inadimplencia": inadimplencia
})

# Preparação dos dados para o modelo
X = df_inadimplencia[["Renda", "Divida_Atual", "Area_Plantada", "Preco_Commodity", "Chuva_Anual"]]
y = df_inadimplencia["Inadimplencia"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# Treinamento do modelo de Random Forest Classifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Previsões e avaliação
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

print("\nModelo de Previsão de Inadimplência (Random Forest - Simulado):")
print("\nRelatório de Classificação:")
print(classification_report(y_test, y_pred))
print(f"AUC-ROC Score: {roc_auc_score(y_test, y_pred_proba):.2f}")

# Insights sobre o modelo
print("\nInsights sobre Modelos de Previsão de Inadimplência:")
print("- O modelo de previsão de inadimplência, utilizando fatores financeiros, agrícolas e climáticos, pode identificar clientes com maior probabilidade de atrasar pagamentos.")
print("- A capacidade de prever a inadimplência permite ao SICOOB agir proativamente, oferecendo renegociações, suporte ou ajustando as condições de crédito para mitigar perdas.")
print("- Em um cenário real, a integração desses modelos com dados históricos e em tempo real do SICOOB seria fundamental para uma gestão de risco mais robusta e eficiente.")

# Salvando os dados simulados em CSV
df_inadimplencia.to_csv("dados_inadimplencia_simulado.csv", index=False)
print("\nDados simulados de inadimplência salvos em \"dados_inadimplencia_simulado.csv\".")


