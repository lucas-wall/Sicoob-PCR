"""
Script de Carregamento para o Power BI
Prepara e carrega dados transformados para o Power BI
"""

import pandas as pd
import json
from datetime import datetime
import logging
import os

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl_log.log', mode='a'),
        logging.StreamHandler()
    ]
)

class PowerBIDataLoader:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.output_dir = 'powerbi_data'
        
    def create_output_directory(self):
        """Cria diretório de saída para os dados do Power BI"""
        try:
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
                self.logger.info(f"Diretório {self.output_dir} criado")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao criar diretório: {e}")
            return False
    
    def load_transformed_data(self):
        """Carrega os dados transformados"""
        try:
            self.logger.info("Carregando dados transformados")
            
            fact_credito = pd.read_csv('fact_credito_rural.csv')
            dim_tempo = pd.read_csv('dim_tempo.csv')
            dim_linha_credito = pd.read_csv('dim_linha_credito.csv')
            dim_cultura = pd.read_csv('dim_cultura.csv')
            dim_cooperativas = pd.read_csv('dim_cooperativas.csv')
            
            self.logger.info(f"Dados carregados: {len(fact_credito)} registros na tabela fato")
            
            return fact_credito, dim_tempo, dim_linha_credito, dim_cultura, dim_cooperativas
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar dados transformados: {e}")
            return None, None, None, None, None
    
    def create_powerbi_measures(self):
        """Cria arquivo com medidas DAX para o Power BI"""
        try:
            self.logger.info("Criando medidas DAX para Power BI")
            
            measures = {
                "Volume Total da Carteira": "SUM(fact_credito_rural[valor_operacao])",
                "Número de Operações": "COUNT(fact_credito_rural[id_operacao])",
                "Ticket Médio": "DIVIDE([Volume Total da Carteira], [Número de Operações])",
                "Taxa de Inadimplência": "DIVIDE(SUM(fact_credito_rural[valor_em_atraso]), [Volume Total da Carteira])",
                "Provisão Total": "SUM(fact_credito_rural[provisao])",
                "Índice de Cobertura": "DIVIDE([Provisão Total], SUM(fact_credito_rural[valor_em_atraso]))",
                "Crescimento da Carteira": """
                VAR VolumeAtual = [Volume Total da Carteira]
                VAR VolumeAnterior = CALCULATE([Volume Total da Carteira], DATEADD(dim_tempo[data], -1, YEAR))
                RETURN DIVIDE(VolumeAtual - VolumeAnterior, VolumeAnterior)
                """,
                "Operações em Atraso": "CALCULATE([Número de Operações], fact_credito_rural[dias_atraso] > 0)",
                "Volume em Atraso": "SUM(fact_credito_rural[valor_em_atraso])",
                "Spread Médio": "AVERAGE(fact_credito_rural[taxa_juros]) - 6.5", # 6.5% como custo de captação simulado
                "ROA": "DIVIDE([Volume Total da Carteira] * 0.02, [Volume Total da Carteira])" # 2% de margem simulada
            }
            
            # Salvar medidas em arquivo JSON
            with open(f'{self.output_dir}/medidas_dax.json', 'w', encoding='utf-8') as f:
                json.dump(measures, f, indent=2, ensure_ascii=False)
            
            self.logger.info("Medidas DAX criadas e salvas")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao criar medidas DAX: {e}")
            return False
    
    def optimize_for_powerbi(self, df, table_name):
        """Otimiza DataFrame para carregamento no Power BI"""
        try:
            self.logger.info(f"Otimizando tabela {table_name} para Power BI")
            
            # Converter tipos de dados para otimizar performance
            for col in df.columns:
                if df[col].dtype == 'object':
                    # Verificar se é data
                    if 'data' in col.lower():
                        try:
                            df[col] = pd.to_datetime(df[col])
                        except:
                            pass
                    else:
                        # Converter para categoria se tiver poucos valores únicos
                        if df[col].nunique() / len(df) < 0.5:
                            df[col] = df[col].astype('category')
                
                elif df[col].dtype in ['int64', 'float64']:
                    # Otimizar tipos numéricos
                    if df[col].dtype == 'int64':
                        if df[col].min() >= 0 and df[col].max() <= 255:
                            df[col] = df[col].astype('uint8')
                        elif df[col].min() >= -32768 and df[col].max() <= 32767:
                            df[col] = df[col].astype('int16')
                        elif df[col].min() >= -2147483648 and df[col].max() <= 2147483647:
                            df[col] = df[col].astype('int32')
                    
                    elif df[col].dtype == 'float64':
                        df[col] = df[col].astype('float32')
            
            self.logger.info(f"Tabela {table_name} otimizada")
            return df
            
        except Exception as e:
            self.logger.error(f"Erro ao otimizar tabela {table_name}: {e}")
            return df
    
    def create_data_model_documentation(self):
        """Cria documentação do modelo de dados"""
        try:
            self.logger.info("Criando documentação do modelo de dados")
            
            documentation = {
                "modelo_dados": {
                    "descricao": "Modelo de dados para análise de crédito rural do SICOOB",
                    "data_criacao": datetime.now().isoformat(),
                    "versao": "1.0"
                },
                "tabelas": {
                    "fact_credito_rural": {
                        "tipo": "Fato",
                        "descricao": "Tabela principal com dados das operações de crédito rural",
                        "relacionamentos": [
                            "dim_tempo (data_contratacao)",
                            "dim_cooperativas (id_cooperativa)",
                            "dim_linha_credito (linha_credito)",
                            "dim_cultura (cultura)"
                        ]
                    },
                    "dim_tempo": {
                        "tipo": "Dimensão",
                        "descricao": "Dimensão temporal para análises por período"
                    },
                    "dim_cooperativas": {
                        "tipo": "Dimensão",
                        "descricao": "Informações das cooperativas do SICOOB"
                    },
                    "dim_linha_credito": {
                        "tipo": "Dimensão",
                        "descricao": "Tipos de linha de crédito rural"
                    },
                    "dim_cultura": {
                        "tipo": "Dimensão",
                        "descricao": "Culturas agrícolas financiadas"
                    }
                },
                "kpis_principais": [
                    "Volume Total da Carteira",
                    "Taxa de Inadimplência",
                    "Número de Operações",
                    "Ticket Médio",
                    "Provisão Total"
                ]
            }
            
            with open(f'{self.output_dir}/documentacao_modelo.json', 'w', encoding='utf-8') as f:
                json.dump(documentation, f, indent=2, ensure_ascii=False)
            
            self.logger.info("Documentação do modelo criada")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao criar documentação: {e}")
            return False
    
    def save_powerbi_ready_data(self, fact_credito, dim_tempo, dim_linha_credito, dim_cultura, dim_cooperativas):
        """Salva dados otimizados para Power BI"""
        try:
            self.logger.info("Salvando dados otimizados para Power BI")
            
            # Otimizar cada tabela
            fact_credito_opt = self.optimize_for_powerbi(fact_credito, 'fact_credito_rural')
            dim_tempo_opt = self.optimize_for_powerbi(dim_tempo, 'dim_tempo')
            dim_linha_credito_opt = self.optimize_for_powerbi(dim_linha_credito, 'dim_linha_credito')
            dim_cultura_opt = self.optimize_for_powerbi(dim_cultura, 'dim_cultura')
            dim_cooperativas_opt = self.optimize_for_powerbi(dim_cooperativas, 'dim_cooperativas')
            
            # Salvar em formato CSV otimizado
            fact_credito_opt.to_csv(f'{self.output_dir}/fact_credito_rural.csv', index=False, encoding='utf-8')
            dim_tempo_opt.to_csv(f'{self.output_dir}/dim_tempo.csv', index=False, encoding='utf-8')
            dim_linha_credito_opt.to_csv(f'{self.output_dir}/dim_linha_credito.csv', index=False, encoding='utf-8')
            dim_cultura_opt.to_csv(f'{self.output_dir}/dim_cultura.csv', index=False, encoding='utf-8')
            dim_cooperativas_opt.to_csv(f'{self.output_dir}/dim_cooperativas.csv', index=False, encoding='utf-8')
            
            # Salvar também em formato Parquet para melhor performance
            fact_credito_opt.to_parquet(f'{self.output_dir}/fact_credito_rural.parquet', index=False)
            dim_tempo_opt.to_parquet(f'{self.output_dir}/dim_tempo.parquet', index=False)
            dim_linha_credito_opt.to_parquet(f'{self.output_dir}/dim_linha_credito.parquet', index=False)
            dim_cultura_opt.to_parquet(f'{self.output_dir}/dim_cultura.parquet', index=False)
            dim_cooperativas_opt.to_parquet(f'{self.output_dir}/dim_cooperativas.parquet', index=False)
            
            self.logger.info("Dados salvos em formato otimizado para Power BI")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar dados para Power BI: {e}")
            return False
    
    def create_refresh_script(self):
        """Cria script de atualização automática"""
        try:
            self.logger.info("Criando script de atualização automática")
            
            refresh_script = """
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
"""
            
            with open(f'{self.output_dir}/refresh_dashboard.py', 'w', encoding='utf-8') as f:
                f.write(refresh_script)
            
            self.logger.info("Script de atualização criado")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao criar script de atualização: {e}")
            return False
    
    def run_loading(self):
        """Executa todo o processo de carregamento"""
        self.logger.info("=== INICIANDO PROCESSO DE CARREGAMENTO PARA POWER BI ===")
        
        # Criar diretório de saída
        if not self.create_output_directory():
            return False
        
        # Carregar dados transformados
        fact_credito, dim_tempo, dim_linha_credito, dim_cultura, dim_cooperativas = self.load_transformed_data()
        if fact_credito is None:
            return False
        
        # Criar medidas DAX
        self.create_powerbi_measures()
        
        # Criar documentação
        self.create_data_model_documentation()
        
        # Salvar dados otimizados
        success = self.save_powerbi_ready_data(fact_credito, dim_tempo, dim_linha_credito, dim_cultura, dim_cooperativas)
        
        # Criar script de atualização
        self.create_refresh_script()
        
        self.logger.info("=== PROCESSO DE CARREGAMENTO CONCLUÍDO ===")
        return success

if __name__ == "__main__":
    loader = PowerBIDataLoader()
    loader.run_loading()

