"""
Script de Extração de Dados do Sistema SICOOB
Simula a extração de dados de crédito rural de diferentes fontes
"""

import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime, timedelta
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl_log.log'),
        logging.StreamHandler()
    ]
)

class SicoobDataExtractor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.connection = None
        
    def connect_to_database(self):
        """Simula conexão com o banco de dados do SICOOB"""
        try:
            # Em um cenário real, seria uma conexão com o banco de dados do SICOOB
            self.connection = sqlite3.connect(':memory:')
            self.logger.info("Conexão com banco de dados estabelecida com sucesso")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao conectar com banco de dados: {e}")
            return False
    
    def extract_carteira_data(self):
        """Extrai dados da carteira de crédito rural"""
        try:
            self.logger.info("Iniciando extração de dados da carteira")
            
            # Simulação de dados da carteira
            np.random.seed(100)
            num_operacoes = 10000
            
            data = {
                'id_operacao': range(1, num_operacoes + 1),
                'id_cooperativa': np.random.randint(1, 51, num_operacoes),
                'id_cliente': np.random.randint(1, 5001, num_operacoes),
                'linha_credito': np.random.choice(['Custeio', 'Investimento', 'Comercialização', 'Pronaf', 'Pronamp'], num_operacoes),
                'cultura': np.random.choice(['Soja', 'Milho', 'Café', 'Cana-de-açúcar', 'Algodão'], num_operacoes),
                'valor_operacao': np.random.normal(250000, 100000, num_operacoes),
                'data_contratacao': [datetime.now() - timedelta(days=np.random.randint(1, 730)) for _ in range(num_operacoes)],
                'data_vencimento': [datetime.now() + timedelta(days=np.random.randint(30, 365)) for _ in range(num_operacoes)],
                'taxa_juros': np.random.normal(8.5, 2.0, num_operacoes),
                'status': np.random.choice(['Ativo', 'Vencido', 'Liquidado'], num_operacoes, p=[0.7, 0.1, 0.2]),
                'dias_atraso': np.random.randint(0, 180, num_operacoes),
                'regiao': np.random.choice(['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul'], num_operacoes),
                'estado': np.random.choice(['MG', 'SP', 'PR', 'GO', 'MT', 'BA', 'RS'], num_operacoes)
            }
            
            df_carteira = pd.DataFrame(data)
            
            # Ajustar valores para serem positivos
            df_carteira['valor_operacao'] = df_carteira['valor_operacao'].apply(lambda x: max(10000, x))
            df_carteira['taxa_juros'] = df_carteira['taxa_juros'].apply(lambda x: max(3.0, min(15.0, x)))
            
            # Ajustar dias de atraso baseado no status
            df_carteira.loc[df_carteira['status'] == 'Ativo', 'dias_atraso'] = 0
            df_carteira.loc[df_carteira['status'] == 'Liquidado', 'dias_atraso'] = 0
            
            self.logger.info(f"Extração concluída: {len(df_carteira)} operações extraídas")
            return df_carteira
            
        except Exception as e:
            self.logger.error(f"Erro na extração de dados da carteira: {e}")
            return None
    
    def extract_cliente_data(self):
        """Extrai dados dos clientes"""
        try:
            self.logger.info("Iniciando extração de dados dos clientes")
            
            # Simulação de dados dos clientes
            np.random.seed(101)
            num_clientes = 5000
            
            data = {
                'id_cliente': range(1, num_clientes + 1),
                'nome_cliente': [f'Cliente_{i}' for i in range(1, num_clientes + 1)],
                'cpf_cnpj': [str(np.random.randint(10**10, 10**11, dtype=np.int64)) for _ in range(num_clientes)],
                'renda_anual': np.random.normal(120000, 50000, num_clientes),
                'area_propriedade': np.random.normal(80, 40, num_clientes),
                'score_credito': np.random.uniform(300, 900, num_clientes),
                'data_cadastro': [datetime.now() - timedelta(days=np.random.randint(1, 1825)) for _ in range(num_clientes)],
                'segmento': np.random.choice(['Pequeno Produtor', 'Médio Produtor', 'Grande Produtor'], num_clientes, p=[0.5, 0.3, 0.2])
            }
            
            df_clientes = pd.DataFrame(data)
            
            # Ajustar valores para serem positivos
            df_clientes['renda_anual'] = df_clientes['renda_anual'].apply(lambda x: max(20000, x))
            df_clientes['area_propriedade'] = df_clientes['area_propriedade'].apply(lambda x: max(1, x))
            
            self.logger.info(f"Extração concluída: {len(df_clientes)} clientes extraídos")
            return df_clientes
            
        except Exception as e:
            self.logger.error(f"Erro na extração de dados dos clientes: {e}")
            return None
    
    def extract_cooperativa_data(self):
        """Extrai dados das cooperativas"""
        try:
            self.logger.info("Iniciando extração de dados das cooperativas")
            
            # Simulação de dados das cooperativas
            cooperativas = [
                {'id_cooperativa': 1, 'nome': 'Sicoob Crediminas', 'estado': 'MG', 'regiao': 'Sudeste'},
                {'id_cooperativa': 2, 'nome': 'Sicoob Credicom', 'estado': 'MG', 'regiao': 'Sudeste'},
                {'id_cooperativa': 3, 'nome': 'Sicoob Cooplivre', 'estado': 'SP', 'regiao': 'Sudeste'},
                {'id_cooperativa': 4, 'nome': 'Sicoob Metropolitano', 'estado': 'PR', 'regiao': 'Sul'},
                {'id_cooperativa': 5, 'nome': 'Sicoob Engecred', 'estado': 'GO', 'regiao': 'Centro-Oeste'},
                # Adicionar mais cooperativas simuladas
            ]
            
            # Expandir para 50 cooperativas
            for i in range(6, 51):
                cooperativas.append({
                    'id_cooperativa': i,
                    'nome': f'Sicoob Regional {i}',
                    'estado': np.random.choice(['MG', 'SP', 'PR', 'GO', 'MT', 'BA', 'RS']),
                    'regiao': np.random.choice(['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul'])
                })
            
            df_cooperativas = pd.DataFrame(cooperativas)
            
            self.logger.info(f"Extração concluída: {len(df_cooperativas)} cooperativas extraídas")
            return df_cooperativas
            
        except Exception as e:
            self.logger.error(f"Erro na extração de dados das cooperativas: {e}")
            return None
    
    def save_to_csv(self, dataframe, filename):
        """Salva DataFrame em arquivo CSV"""
        try:
            dataframe.to_csv(filename, index=False, encoding='utf-8')
            self.logger.info(f"Dados salvos em {filename}")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao salvar arquivo {filename}: {e}")
            return False
    
    def run_extraction(self):
        """Executa todo o processo de extração"""
        self.logger.info("=== INICIANDO PROCESSO DE EXTRAÇÃO DE DADOS ===")
        
        if not self.connect_to_database():
            return False
        
        # Extrair dados da carteira
        df_carteira = self.extract_carteira_data()
        if df_carteira is not None:
            self.save_to_csv(df_carteira, 'dados_carteira_extraidos.csv')
        
        # Extrair dados dos clientes
        df_clientes = self.extract_cliente_data()
        if df_clientes is not None:
            self.save_to_csv(df_clientes, 'dados_clientes_extraidos.csv')
        
        # Extrair dados das cooperativas
        df_cooperativas = self.extract_cooperativa_data()
        if df_cooperativas is not None:
            self.save_to_csv(df_cooperativas, 'dados_cooperativas_extraidos.csv')
        
        self.logger.info("=== PROCESSO DE EXTRAÇÃO CONCLUÍDO ===")
        return True

if __name__ == "__main__":
    extractor = SicoobDataExtractor()
    extractor.run_extraction()

