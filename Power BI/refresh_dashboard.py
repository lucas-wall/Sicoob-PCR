
# Script de Atualização Automática do Dashboard SICOOB
# Execute este script para atualizar os dados do Power BI

import subprocess
import sys
from datetime import datetime

def run_etl_pipeline():
    try:
        print(f"Iniciando atualização em {datetime.now()}")
        
        # Executar extração
        result = subprocess.run([sys.executable, 'script_extracao_dados.py'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Erro na extração: {result.stderr}")
            return False
        
        # Executar transformação
        result = subprocess.run([sys.executable, 'script_transformacao_dados.py'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Erro na transformação: {result.stderr}")
            return False
        
        # Executar carregamento
        result = subprocess.run([sys.executable, 'script_carregamento_powerbi.py'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Erro no carregamento: {result.stderr}")
            return False
        
        print(f"Atualização concluída com sucesso em {datetime.now()}")
        return True
        
    except Exception as e:
        print(f"Erro na atualização: {e}")
        return False

if __name__ == "__main__":
    run_etl_pipeline()
