
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score

# Simulação de dados para modelos de score de crédito

np.random.seed(55)

num_clientes = 1000

# Geração de dados simulados
renda = np.random.normal(loc=5000, scale=2000, size=num_clientes) # Renda mensal
divida = np.random.normal(loc=1000, scale=500, size=num_clientes) # Dívida atual
historico_bom_pagador = np.random.randint(0, 2, size=num_clientes) # 0=ruim, 1=bom

# Geração da variável alvo (inadimplência): 0=adimplente, 1=inadimplente
# A inadimplência é mais provável com baixa renda, alta dívida e histórico ruim
inadimplencia_prob = 1 / (1 + np.exp(0.001 * renda - 0.005 * divida + 2 * historico_bom_pagador - 3))
inadimplencia = (np.random.rand(num_clientes) < inadimplencia_prob).astype(int)

df_credito = pd.DataFrame({
    "Renda": renda,
    "Divida": divida,
    "Historico_Bom_Pagador": historico_bom_pagador,
    "Inadimplencia": inadimplencia
})

# Garantir que haja pelo menos uma ocorrência de cada classe na variável alvo
if df_credito["Inadimplencia"].nunique() < 2:
    df_credito.loc[0, "Inadimplencia"] = 0
    df_credito.loc[1, "Inadimplencia"] = 1

# Preparação dos dados para o modelo
X = df_credito[["Renda", "Divida", "Historico_Bom_Pagador"]]
y = df_credito["Inadimplencia"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Treinamento do modelo de Regressão Logística
model = LogisticRegression(random_state=42)
model.fit(X_train, y_train)

# Previsões e avaliação
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

print("\nModelo de Score de Crédito (Regressão Logística - Simulado):")
print("\nRelatório de Classificação:")
print(classification_report(y_test, y_pred))
print(f"AUC-ROC Score: {roc_auc_score(y_test, y_pred_proba):.2f}")

# Insights sobre o modelo
print("\nInsights sobre Modelos de Score de Crédito:")
print("- O modelo de score de crédito, mesmo com dados simulados, demonstra a capacidade de prever a probabilidade de inadimplência dos clientes.")
print("- Métricas como Precisão, Recall, F1-Score e AUC-ROC são essenciais para avaliar a performance do modelo e sua capacidade de identificar bons e maus pagadores.")
print("- Em um cenário real, esses modelos seriam treinados com dados históricos de crédito do SICOOB, permitindo uma avaliação mais precisa do risco e a tomada de decisões mais assertivas na concessão de crédito.")

# Salvando os dados simulados em CSV
df_credito.to_csv("dados_credito_simulado.csv", index=False)
print("\nDados simulados de crédito salvos em \"dados_credito_simulado.csv\".")


