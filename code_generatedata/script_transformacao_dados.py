"""
Script de Transformação e Limpeza de Dados
Processa os dados extraídos do sistema SICOOB para análise
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl_log.log', mode='a'),
        logging.StreamHandler()
    ]
)

class SicoobDataTransformer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def load_extracted_data(self):
        """Carrega os dados extraídos"""
        try:
            self.logger.info("Carregando dados extraídos")
            
            df_carteira = pd.read_csv('dados_carteira_extraidos.csv')
            df_clientes = pd.read_csv('dados_clientes_extraidos.csv')
            df_cooperativas = pd.read_csv('dados_cooperativas_extraidos.csv')
            
            self.logger.info(f"Dados carregados: {len(df_carteira)} operações, {len(df_clientes)} clientes, {len(df_cooperativas)} cooperativas")
            
            return df_carteira, df_clientes, df_cooperativas
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar dados extraídos: {e}")
            return None, None, None
    
    def clean_carteira_data(self, df_carteira):
        """Limpa e transforma dados da carteira"""
        try:
            self.logger.info("Iniciando limpeza de dados da carteira")
            
            # Converter datas
            df_carteira['data_contratacao'] = pd.to_datetime(df_carteira['data_contratacao'])
            df_carteira['data_vencimento'] = pd.to_datetime(df_carteira['data_vencimento'])
            
            # Criar colunas derivadas
            df_carteira['ano_contratacao'] = df_carteira['data_contratacao'].dt.year
            df_carteira['mes_contratacao'] = df_carteira['data_contratacao'].dt.month
            df_carteira['trimestre_contratacao'] = df_carteira['data_contratacao'].dt.quarter
            
            # Classificar inadimplência
            df_carteira['inadimplente'] = (df_carteira['dias_atraso'] > 90).astype(int)
            
            # Classificar faixa de atraso
            def classificar_atraso(dias):
                if dias == 0:
                    return 'Em dia'
                elif dias <= 30:
                    return '1-30 dias'
                elif dias <= 60:
                    return '31-60 dias'
                elif dias <= 90:
                    return '61-90 dias'
                else:
                    return 'Acima de 90 dias'
            
            df_carteira['faixa_atraso'] = df_carteira['dias_atraso'].apply(classificar_atraso)
            
            # Classificar valor da operação
            def classificar_valor(valor):
                if valor <= 50000:
                    return 'Pequeno'
                elif valor <= 200000:
                    return 'Médio'
                else:
                    return 'Grande'
            
            df_carteira['porte_operacao'] = df_carteira['valor_operacao'].apply(classificar_valor)
            
            # Remover outliers de taxa de juros
            q1 = df_carteira['taxa_juros'].quantile(0.25)
            q3 = df_carteira['taxa_juros'].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            df_carteira = df_carteira[
                (df_carteira['taxa_juros'] >= lower_bound) & 
                (df_carteira['taxa_juros'] <= upper_bound)
            ]
            
            self.logger.info(f"Limpeza concluída: {len(df_carteira)} operações após limpeza")
            return df_carteira
            
        except Exception as e:
            self.logger.error(f"Erro na limpeza de dados da carteira: {e}")
            return None
    
    def clean_cliente_data(self, df_clientes):
        """Limpa e transforma dados dos clientes"""
        try:
            self.logger.info("Iniciando limpeza de dados dos clientes")
            
            # Converter datas
            df_clientes['data_cadastro'] = pd.to_datetime(df_clientes['data_cadastro'])
            
            # Criar colunas derivadas
            df_clientes['anos_relacionamento'] = (datetime.now() - df_clientes['data_cadastro']).dt.days / 365.25
            
            # Classificar score de crédito
            def classificar_score(score):
                if score < 400:
                    return 'Muito Baixo'
                elif score < 500:
                    return 'Baixo'
                elif score < 650:
                    return 'Médio'
                elif score < 750:
                    return 'Bom'
                else:
                    return 'Excelente'
            
            df_clientes['categoria_score'] = df_clientes['score_credito'].apply(classificar_score)
            
            # Classificar área da propriedade
            def classificar_area(area):
                if area <= 20:
                    return 'Pequena'
                elif area <= 100:
                    return 'Média'
                else:
                    return 'Grande'
            
            df_clientes['porte_propriedade'] = df_clientes['area_propriedade'].apply(classificar_area)
            
            # Remover outliers de renda
            q1 = df_clientes['renda_anual'].quantile(0.25)
            q3 = df_clientes['renda_anual'].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            df_clientes = df_clientes[
                (df_clientes['renda_anual'] >= lower_bound) & 
                (df_clientes['renda_anual'] <= upper_bound)
            ]
            
            self.logger.info(f"Limpeza concluída: {len(df_clientes)} clientes após limpeza")
            return df_clientes
            
        except Exception as e:
            self.logger.error(f"Erro na limpeza de dados dos clientes: {e}")
            return None
    
    def create_fact_table(self, df_carteira, df_clientes, df_cooperativas):
        """Cria tabela fato consolidada"""
        try:
            self.logger.info("Criando tabela fato consolidada")
            
            # Juntar dados da carteira com clientes
            df_fact = df_carteira.merge(df_clientes, on='id_cliente', how='left')
            
            # Juntar com cooperativas
            df_fact = df_fact.merge(df_cooperativas, on='id_cooperativa', how='left')
            
            # Criar métricas agregadas
            df_fact['valor_em_atraso'] = df_fact.apply(
                lambda row: row['valor_operacao'] if row['inadimplente'] == 1 else 0, axis=1
            )
            
            # Calcular provisão (simulada)
            def calcular_provisao(dias_atraso, valor):
                if dias_atraso == 0:
                    return valor * 0.005  # 0.5% para operações em dia
                elif dias_atraso <= 30:
                    return valor * 0.01   # 1% para 1-30 dias
                elif dias_atraso <= 60:
                    return valor * 0.03   # 3% para 31-60 dias
                elif dias_atraso <= 90:
                    return valor * 0.10   # 10% para 61-90 dias
                else:
                    return valor * 0.30   # 30% para acima de 90 dias
            
            df_fact['provisao'] = df_fact.apply(
                lambda row: calcular_provisao(row['dias_atraso'], row['valor_operacao']), axis=1
            )
            
            self.logger.info(f"Tabela fato criada: {len(df_fact)} registros")
            return df_fact
            
        except Exception as e:
            self.logger.error(f"Erro na criação da tabela fato: {e}")
            return None
    
    def create_dimension_tables(self, df_cooperativas):
        """Cria tabelas dimensão"""
        try:
            self.logger.info("Criando tabelas dimensão")
            
            # Dimensão Tempo
            start_date = datetime(2023, 1, 1)
            end_date = datetime(2025, 12, 31)
            date_range = pd.date_range(start=start_date, end=end_date, freq='D')
            
            dim_tempo = pd.DataFrame({
                'data': date_range,
                'ano': date_range.year,
                'mes': date_range.month,
                'trimestre': date_range.quarter,
                'dia_semana': date_range.dayofweek,
                'nome_mes': date_range.strftime('%B'),
                'nome_dia_semana': date_range.strftime('%A')
            })
            
            # Dimensão Linha de Crédito
            dim_linha_credito = pd.DataFrame({
                'linha_credito': ['Custeio', 'Investimento', 'Comercialização', 'Pronaf', 'Pronamp'],
                'categoria': ['Operacional', 'Estrutural', 'Comercial', 'Familiar', 'Médio Porte'],
                'descricao': [
                    'Financiamento para custeio da produção',
                    'Financiamento para investimentos fixos',
                    'Financiamento para comercialização',
                    'Programa Nacional de Fortalecimento da Agricultura Familiar',
                    'Programa Nacional de Apoio ao Médio Produtor Rural'
                ]
            })
            
            # Dimensão Cultura
            dim_cultura = pd.DataFrame({
                'cultura': ['Soja', 'Milho', 'Café', 'Cana-de-açúcar', 'Algodão'],
                'tipo': ['Grão', 'Grão', 'Permanente', 'Semi-permanente', 'Fibra'],
                'sazonalidade': ['Verão', 'Verão/Inverno', 'Ano todo', 'Ano todo', 'Verão']
            })
            
            self.logger.info("Tabelas dimensão criadas")
            return dim_tempo, dim_linha_credito, dim_cultura, df_cooperativas
            
        except Exception as e:
            self.logger.error(f"Erro na criação das tabelas dimensão: {e}")
            return None, None, None, None
    
    def save_transformed_data(self, df_fact, dim_tempo, dim_linha_credito, dim_cultura, dim_cooperativas):
        """Salva dados transformados"""
        try:
            self.logger.info("Salvando dados transformados")
            
            df_fact.to_csv('fact_credito_rural.csv', index=False, encoding='utf-8')
            dim_tempo.to_csv('dim_tempo.csv', index=False, encoding='utf-8')
            dim_linha_credito.to_csv('dim_linha_credito.csv', index=False, encoding='utf-8')
            dim_cultura.to_csv('dim_cultura.csv', index=False, encoding='utf-8')
            dim_cooperativas.to_csv('dim_cooperativas.csv', index=False, encoding='utf-8')
            
            self.logger.info("Dados transformados salvos com sucesso")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar dados transformados: {e}")
            return False
    
    def run_transformation(self):
        """Executa todo o processo de transformação"""
        self.logger.info("=== INICIANDO PROCESSO DE TRANSFORMAÇÃO DE DADOS ===")
        
        # Carregar dados extraídos
        df_carteira, df_clientes, df_cooperativas = self.load_extracted_data()
        if df_carteira is None:
            return False
        
        # Limpar dados
        df_carteira_clean = self.clean_carteira_data(df_carteira)
        df_clientes_clean = self.clean_cliente_data(df_clientes)
        
        if df_carteira_clean is None or df_clientes_clean is None:
            return False
        
        # Criar tabela fato
        df_fact = self.create_fact_table(df_carteira_clean, df_clientes_clean, df_cooperativas)
        if df_fact is None:
            return False
        
        # Criar tabelas dimensão
        dim_tempo, dim_linha_credito, dim_cultura, dim_cooperativas = self.create_dimension_tables(df_cooperativas)
        if dim_tempo is None:
            return False
        
        # Salvar dados transformados
        success = self.save_transformed_data(df_fact, dim_tempo, dim_linha_credito, dim_cultura, dim_cooperativas)
        
        self.logger.info("=== PROCESSO DE TRANSFORMAÇÃO CONCLUÍDO ===")
        return success

if __name__ == "__main__":
    transformer = SicoobDataTransformer()
    transformer.run_transformation()

