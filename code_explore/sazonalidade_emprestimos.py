
import pandas as pd
import numpy as np

# Simulação de dados de sazonalidade dos empréstimos por cultura

np.random.seed(43)

meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
culturas = ['Soja', 'Milho', 'Café', 'Cana-de-açúcar', 'Algodão']

# Simulação de volume de empréstimos (em milhões de R$) por cultura e mês
data = []
for mes_idx, mes in enumerate(meses):
    for cultura in culturas:
        # Base de empréstimos para cada cultura
        if cultura == 'Soja':
            base_emprestimo = 500
            # Pico de empréstimos antes do plantio (Set-Nov) e antes da colheita (Mar-Mai)
            sazonalidade = {
                'Set': 1.5, 'Out': 1.8, 'Nov': 1.6, # Plantio
                'Mar': 1.3, 'Abr': 1.4, 'Mai': 1.2  # Custeio/Colheita
            }
        elif cultura == 'Milho':
            base_emprestimo = 400
            # Pico de empréstimos antes do plantio (Set-Nov para 1a safra, Jan-Fev para 2a safra)
            sazonalidade = {
                'Set': 1.4, 'Out': 1.6, 'Nov': 1.3, # 1a safra
                'Jan': 1.2, 'Fev': 1.5              # 2a safra
            }
        elif cultura == 'Café':
            base_emprestimo = 200
            # Pico de empréstimos antes da colheita (Mai-Jul)
            sazonalidade = {
                'Mai': 1.3, 'Jun': 1.5, 'Jul': 1.2
            }
        elif cultura == 'Cana-de-açúcar':
            base_emprestimo = 300
            # Empréstimos mais distribuídos, com picos no início da safra (Abr-Mai) e final (Set-Out)
            sazonalidade = {
                'Abr': 1.2, 'Mai': 1.3, 'Set': 1.1, 'Out': 1.2
            }
        elif cultura == 'Algodão':
            base_emprestimo = 250
            # Pico de empréstimos antes do plantio (Out-Dez) e antes da colheita (Abr-Jun)
            sazonalidade = {
                'Out': 1.3, 'Nov': 1.4, 'Dez': 1.2, # Plantio
                'Abr': 1.1, 'Mai': 1.2, 'Jun': 1.0  # Custeio/Colheita
            }

        fator_sazonalidade = sazonalidade.get(mes, 1.0) # Fator 1.0 se não houver sazonalidade específica
        volume = base_emprestimo * fator_sazonalidade * np.random.uniform(0.9, 1.1) # Adiciona ruído
        data.append([mes, cultura, round(volume, 2)])

df_sazonalidade = pd.DataFrame(data, columns=['Mês', 'Cultura', 'Volume_Emprestimos_Milhoes_R$'])

print("Sazonalidade dos Empréstimos por Cultura (Simulada):")
print(df_sazonalidade.pivot_table(index='Mês', columns='Cultura', values='Volume_Emprestimos_Milhoes_R$').fillna(0).to_markdown())

# Insights sobre sazonalidade
print("\nInsights sobre Sazonalidade dos Empréstimos:")
print("- A análise da sazonalidade dos empréstimos por cultura revela picos de demanda em períodos específicos do ciclo produtivo, como antes do plantio e da colheita.")
print("- Culturas como Soja e Milho apresentam maior volume de empréstimos, com demandas concentradas em meses estratégicos para o custeio e investimento.")
print("- O SICOOB pode otimizar a alocação de recursos e o planejamento de suas operações de crédito rural ao antecipar essas demandas sazonais, garantindo a disponibilidade de fundos nos momentos certos para cada cultura.")

# Salvando os dados simulados em CSV
df_sazonalidade.to_csv("sazonalidade_emprestimos_simulado.csv", index=False)
print("\nDados simulados de sazonalidade salvos em 'sazonalidade_emprestimos_simulado.csv'.")


