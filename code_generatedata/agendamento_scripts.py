"""
Script de Agendamento de Execução dos Scripts ETL
Configura e executa o pipeline ETL de forma automatizada
"""

import schedule
import time
import subprocess
import sys
import logging
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler_log.log'),
        logging.StreamHandler()
    ]
)

class ETLScheduler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.email_config = {
            'smtp_server': 'smtp.gmail.com',  # Configurar conforme necessário
            'smtp_port': 587,
            'email_user': 'dashboard@sicoob.com.br',  # Email fictício
            'email_password': 'senha_app',  # Senha de app fictícia
            'recipients': ['ti@sicoob.com.br', 'gestao@sicoob.com.br']  # Emails fictícios
        }
    
    def send_notification(self, subject, message, is_error=False):
        """Envia notificação por email"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config['email_user']
            msg['To'] = ', '.join(self.email_config['recipients'])
            msg['Subject'] = f"[SICOOB Dashboard] {subject}"
            
            # Adicionar prioridade se for erro
            if is_error:
                msg['X-Priority'] = '1'
            
            body = f"""
            Dashboard de Crédito Rural - SICOOB
            
            {message}
            
            Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
            
            ---
            Este é um email automático do sistema de ETL do Dashboard SICOOB.
            """
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Em um ambiente real, descomentar as linhas abaixo
            # server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            # server.starttls()
            # server.login(self.email_config['email_user'], self.email_config['email_password'])
            # server.send_message(msg)
            # server.quit()
            
            self.logger.info(f"Notificação enviada: {subject}")
            
        except Exception as e:
            self.logger.error(f"Erro ao enviar notificação: {e}")
    
    def run_etl_pipeline(self):
        """Executa o pipeline ETL completo"""
        try:
            self.logger.info("=== INICIANDO EXECUÇÃO AGENDADA DO PIPELINE ETL ===")
            start_time = datetime.now()
            
            # Executar extração
            self.logger.info("Executando script de extração...")
            result = subprocess.run([sys.executable, 'script_extracao_dados.py'], 
                                  capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                error_msg = f"Erro na extração de dados: {result.stderr}"
                self.logger.error(error_msg)
                self.send_notification("Erro na Extração de Dados", error_msg, is_error=True)
                return False
            
            # Executar transformação
            self.logger.info("Executando script de transformação...")
            result = subprocess.run([sys.executable, 'script_transformacao_dados.py'], 
                                  capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                error_msg = f"Erro na transformação de dados: {result.stderr}"
                self.logger.error(error_msg)
                self.send_notification("Erro na Transformação de Dados", error_msg, is_error=True)
                return False
            
            # Executar carregamento
            self.logger.info("Executando script de carregamento...")
            result = subprocess.run([sys.executable, 'script_carregamento_powerbi.py'], 
                                  capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                error_msg = f"Erro no carregamento para Power BI: {result.stderr}"
                self.logger.error(error_msg)
                self.send_notification("Erro no Carregamento para Power BI", error_msg, is_error=True)
                return False
            
            # Calcular tempo de execução
            end_time = datetime.now()
            execution_time = end_time - start_time
            
            success_msg = f"Pipeline ETL executado com sucesso em {execution_time.total_seconds():.2f} segundos"
            self.logger.info(success_msg)
            self.send_notification("Pipeline ETL Executado com Sucesso", success_msg)
            
            self.logger.info("=== EXECUÇÃO AGENDADA CONCLUÍDA COM SUCESSO ===")
            return True
            
        except subprocess.TimeoutExpired:
            error_msg = "Timeout na execução do pipeline ETL"
            self.logger.error(error_msg)
            self.send_notification("Timeout no Pipeline ETL", error_msg, is_error=True)
            return False
            
        except Exception as e:
            error_msg = f"Erro inesperado no pipeline ETL: {e}"
            self.logger.error(error_msg)
            self.send_notification("Erro Inesperado no Pipeline ETL", error_msg, is_error=True)
            return False
    
    def health_check(self):
        """Verifica a saúde do sistema"""
        try:
            self.logger.info("Executando verificação de saúde do sistema")
            
            # Verificar se os arquivos necessários existem
            required_files = [
                'script_extracao_dados.py',
                'script_transformacao_dados.py',
                'script_carregamento_powerbi.py'
            ]
            
            missing_files = []
            for file in required_files:
                try:
                    with open(file, 'r'):
                        pass
                except FileNotFoundError:
                    missing_files.append(file)
            
            if missing_files:
                error_msg = f"Arquivos necessários não encontrados: {', '.join(missing_files)}"
                self.logger.error(error_msg)
                self.send_notification("Erro na Verificação de Saúde", error_msg, is_error=True)
                return False
            
            # Verificar espaço em disco (simulado)
            # Em um ambiente real, usar shutil.disk_usage()
            disk_usage_percent = 75  # Simulado
            if disk_usage_percent > 90:
                warning_msg = f"Espaço em disco baixo: {disk_usage_percent}% utilizado"
                self.logger.warning(warning_msg)
                self.send_notification("Aviso: Espaço em Disco Baixo", warning_msg)
            
            self.logger.info("Verificação de saúde concluída com sucesso")
            return True
            
        except Exception as e:
            error_msg = f"Erro na verificação de saúde: {e}"
            self.logger.error(error_msg)
            self.send_notification("Erro na Verificação de Saúde", error_msg, is_error=True)
            return False
    
    def setup_schedule(self):
        """Configura os agendamentos"""
        try:
            self.logger.info("Configurando agendamentos...")
            
            # Pipeline ETL completo - diário às 06:00
            schedule.every().day.at("06:00").do(self.run_etl_pipeline)
            
            # Verificação de saúde - a cada 4 horas
            schedule.every(4).hours.do(self.health_check)
            
            # Pipeline ETL adicional - segunda-feira às 08:00 (para dados da semana)
            schedule.every().monday.at("08:00").do(self.run_etl_pipeline)
            
            self.logger.info("Agendamentos configurados:")
            self.logger.info("- Pipeline ETL: Diário às 06:00")
            self.logger.info("- Pipeline ETL: Segunda-feira às 08:00")
            self.logger.info("- Verificação de saúde: A cada 4 horas")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao configurar agendamentos: {e}")
            return False
    
    def run_scheduler(self):
        """Executa o agendador"""
        try:
            self.logger.info("=== INICIANDO AGENDADOR ETL ===")
            
            if not self.setup_schedule():
                return False
            
            # Enviar notificação de início
            self.send_notification("Agendador ETL Iniciado", "O agendador do pipeline ETL foi iniciado com sucesso")
            
            # Executar verificação inicial
            self.health_check()
            
            self.logger.info("Agendador em execução. Pressione Ctrl+C para parar.")
            
            while True:
                schedule.run_pending()
                time.sleep(60)  # Verificar a cada minuto
                
        except KeyboardInterrupt:
            self.logger.info("Agendador interrompido pelo usuário")
            self.send_notification("Agendador ETL Parado", "O agendador do pipeline ETL foi interrompido")
            
        except Exception as e:
            error_msg = f"Erro no agendador: {e}"
            self.logger.error(error_msg)
            self.send_notification("Erro no Agendador ETL", error_msg, is_error=True)
    
    def run_manual_execution(self):
        """Executa o pipeline manualmente para teste"""
        self.logger.info("=== EXECUÇÃO MANUAL DO PIPELINE ETL ===")
        success = self.run_etl_pipeline()
        if success:
            self.logger.info("Execução manual concluída com sucesso")
        else:
            self.logger.error("Execução manual falhou")
        return success

if __name__ == "__main__":
    scheduler = ETLScheduler()
    
    # Verificar se foi solicitada execução manual
    if len(sys.argv) > 1 and sys.argv[1] == "--manual":
        scheduler.run_manual_execution()
    else:
        # Instalar a biblioteca schedule se não estiver instalada
        try:
            import schedule
        except ImportError:
            print("Instalando biblioteca schedule...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "schedule"])
            import schedule
        
        scheduler.run_scheduler()

