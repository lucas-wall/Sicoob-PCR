"""
Script de Monitoramento e Alertas de Falhas
Sistema de monitoramento para o pipeline ETL do SICOOB
"""

import os
import json
import time
import psutil
import logging
from datetime import datetime, timedelta
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('monitoring_log.log'),
        logging.StreamHandler()
    ]
)

class ETLMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.config_file = 'monitoring_config.json'
        self.status_file = 'etl_status.json'
        self.load_config()
        
    def load_config(self):
        """Carrega configurações de monitoramento"""
        default_config = {
            "thresholds": {
                "disk_usage_warning": 80,
                "disk_usage_critical": 90,
                "memory_usage_warning": 80,
                "memory_usage_critical": 90,
                "cpu_usage_warning": 80,
                "cpu_usage_critical": 90,
                "etl_timeout_minutes": 30,
                "file_age_hours": 25
            },
            "email": {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "email_user": "monitoring@sicoob.com.br",
                "email_password": "senha_app",
                "recipients": ["ti@sicoob.com.br", "gestao@sicoob.com.br"]
            },
            "files_to_monitor": [
                "dados_carteira_extraidos.csv",
                "fact_credito_rural.csv",
                "powerbi_data/fact_credito_rural.csv"
            ],
            "logs_to_monitor": [
                "etl_log.log",
                "scheduler_log.log"
            ]
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.config = default_config
                self.save_config()
                
        except Exception as e:
            self.logger.error(f"Erro ao carregar configuração: {e}")
            self.config = default_config
    
    def save_config(self):
        """Salva configurações"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Erro ao salvar configuração: {e}")
    
    def send_alert(self, subject, message, level="INFO"):
        """Envia alerta por email"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config['email']['email_user']
            msg['To'] = ', '.join(self.config['email']['recipients'])
            msg['Subject'] = f"[SICOOB ETL {level}] {subject}"
            
            if level == "CRITICAL":
                msg['X-Priority'] = '1'
            elif level == "WARNING":
                msg['X-Priority'] = '3'
            
            body = f"""
            Sistema de Monitoramento ETL - SICOOB
            
            Nível: {level}
            Assunto: {subject}
            
            Detalhes:
            {message}
            
            Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
            
            ---
            Este é um alerta automático do sistema de monitoramento ETL.
            """
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Em um ambiente real, descomentar as linhas abaixo
            # server = smtplib.SMTP(self.config['email']['smtp_server'], self.config['email']['smtp_port'])
            # server.starttls()
            # server.login(self.config['email']['email_user'], self.config['email']['email_password'])
            # server.send_message(msg)
            # server.quit()
            
            self.logger.info(f"Alerta enviado [{level}]: {subject}")
            
        except Exception as e:
            self.logger.error(f"Erro ao enviar alerta: {e}")
    
    def check_system_resources(self):
        """Verifica recursos do sistema"""
        try:
            alerts = []
            
            # Verificar uso de disco
            disk_usage = psutil.disk_usage('/').percent
            if disk_usage >= self.config['thresholds']['disk_usage_critical']:
                alerts.append({
                    'level': 'CRITICAL',
                    'subject': 'Espaço em Disco Crítico',
                    'message': f'Uso de disco: {disk_usage:.1f}%'
                })
            elif disk_usage >= self.config['thresholds']['disk_usage_warning']:
                alerts.append({
                    'level': 'WARNING',
                    'subject': 'Espaço em Disco Alto',
                    'message': f'Uso de disco: {disk_usage:.1f}%'
                })
            
            # Verificar uso de memória
            memory_usage = psutil.virtual_memory().percent
            if memory_usage >= self.config['thresholds']['memory_usage_critical']:
                alerts.append({
                    'level': 'CRITICAL',
                    'subject': 'Uso de Memória Crítico',
                    'message': f'Uso de memória: {memory_usage:.1f}%'
                })
            elif memory_usage >= self.config['thresholds']['memory_usage_warning']:
                alerts.append({
                    'level': 'WARNING',
                    'subject': 'Uso de Memória Alto',
                    'message': f'Uso de memória: {memory_usage:.1f}%'
                })
            
            # Verificar uso de CPU (média dos últimos 5 segundos)
            cpu_usage = psutil.cpu_percent(interval=5)
            if cpu_usage >= self.config['thresholds']['cpu_usage_critical']:
                alerts.append({
                    'level': 'CRITICAL',
                    'subject': 'Uso de CPU Crítico',
                    'message': f'Uso de CPU: {cpu_usage:.1f}%'
                })
            elif cpu_usage >= self.config['thresholds']['cpu_usage_warning']:
                alerts.append({
                    'level': 'WARNING',
                    'subject': 'Uso de CPU Alto',
                    'message': f'Uso de CPU: {cpu_usage:.1f}%'
                })
            
            # Enviar alertas
            for alert in alerts:
                self.send_alert(alert['subject'], alert['message'], alert['level'])
            
            self.logger.info(f"Verificação de recursos: Disco {disk_usage:.1f}%, Memória {memory_usage:.1f}%, CPU {cpu_usage:.1f}%")
            return len(alerts) == 0
            
        except Exception as e:
            self.logger.error(f"Erro na verificação de recursos: {e}")
            return False
    
    def check_file_integrity(self):
        """Verifica integridade dos arquivos"""
        try:
            alerts = []
            
            for file_path in self.config['files_to_monitor']:
                if not os.path.exists(file_path):
                    alerts.append({
                        'level': 'CRITICAL',
                        'subject': 'Arquivo Não Encontrado',
                        'message': f'Arquivo obrigatório não encontrado: {file_path}'
                    })
                    continue
                
                # Verificar idade do arquivo
                file_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(file_path))
                max_age = timedelta(hours=self.config['thresholds']['file_age_hours'])
                
                if file_age > max_age:
                    alerts.append({
                        'level': 'WARNING',
                        'subject': 'Arquivo Desatualizado',
                        'message': f'Arquivo {file_path} não foi atualizado há {file_age.total_seconds()/3600:.1f} horas'
                    })
                
                # Verificar tamanho do arquivo
                file_size = os.path.getsize(file_path)
                if file_size == 0:
                    alerts.append({
                        'level': 'CRITICAL',
                        'subject': 'Arquivo Vazio',
                        'message': f'Arquivo {file_path} está vazio'
                    })
            
            # Enviar alertas
            for alert in alerts:
                self.send_alert(alert['subject'], alert['message'], alert['level'])
            
            self.logger.info(f"Verificação de arquivos: {len(self.config['files_to_monitor'])} arquivos verificados, {len(alerts)} alertas")
            return len(alerts) == 0
            
        except Exception as e:
            self.logger.error(f"Erro na verificação de arquivos: {e}")
            return False
    
    def check_log_errors(self):
        """Verifica erros nos logs"""
        try:
            alerts = []
            
            for log_file in self.config['logs_to_monitor']:
                if not os.path.exists(log_file):
                    continue
                
                # Ler últimas linhas do log
                try:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    # Verificar últimas 100 linhas por erros
                    recent_lines = lines[-100:] if len(lines) > 100 else lines
                    error_count = 0
                    critical_errors = []
                    
                    for line in recent_lines:
                        if 'ERROR' in line:
                            error_count += 1
                            if error_count <= 3:  # Mostrar apenas os 3 primeiros erros
                                critical_errors.append(line.strip())
                    
                    if error_count > 0:
                        alerts.append({
                            'level': 'WARNING' if error_count < 5 else 'CRITICAL',
                            'subject': f'Erros Detectados no Log {log_file}',
                            'message': f'{error_count} erros encontrados. Exemplos:\n' + '\n'.join(critical_errors)
                        })
                
                except Exception as e:
                    self.logger.error(f"Erro ao ler log {log_file}: {e}")
            
            # Enviar alertas
            for alert in alerts:
                self.send_alert(alert['subject'], alert['message'], alert['level'])
            
            self.logger.info(f"Verificação de logs: {len(self.config['logs_to_monitor'])} logs verificados, {len(alerts)} alertas")
            return len(alerts) == 0
            
        except Exception as e:
            self.logger.error(f"Erro na verificação de logs: {e}")
            return False
    
    def update_status(self, status_data):
        """Atualiza arquivo de status"""
        try:
            status_data['last_update'] = datetime.now().isoformat()
            with open(self.status_file, 'w', encoding='utf-8') as f:
                json.dump(status_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Erro ao atualizar status: {e}")
    
    def get_status(self):
        """Obtém status atual"""
        try:
            if os.path.exists(self.status_file):
                with open(self.status_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            self.logger.error(f"Erro ao obter status: {e}")
            return {}
    
    def run_full_check(self):
        """Executa verificação completa"""
        try:
            self.logger.info("=== INICIANDO VERIFICAÇÃO COMPLETA ===")
            
            status = {
                'check_time': datetime.now().isoformat(),
                'system_resources': self.check_system_resources(),
                'file_integrity': self.check_file_integrity(),
                'log_errors': self.check_log_errors()
            }
            
            status['overall_health'] = all([
                status['system_resources'],
                status['file_integrity'],
                status['log_errors']
            ])
            
            self.update_status(status)
            
            if status['overall_health']:
                self.logger.info("Sistema saudável - todas as verificações passaram")
            else:
                self.logger.warning("Problemas detectados no sistema")
            
            self.logger.info("=== VERIFICAÇÃO COMPLETA CONCLUÍDA ===")
            return status['overall_health']
            
        except Exception as e:
            self.logger.error(f"Erro na verificação completa: {e}")
            return False
    
    def run_continuous_monitoring(self, interval_minutes=15):
        """Executa monitoramento contínuo"""
        try:
            self.logger.info(f"=== INICIANDO MONITORAMENTO CONTÍNUO (Intervalo: {interval_minutes} minutos) ===")
            
            while True:
                self.run_full_check()
                self.logger.info(f"Próxima verificação em {interval_minutes} minutos...")
                time.sleep(interval_minutes * 60)
                
        except KeyboardInterrupt:
            self.logger.info("Monitoramento interrompido pelo usuário")
        except Exception as e:
            self.logger.error(f"Erro no monitoramento contínuo: {e}")

if __name__ == "__main__":
    import sys
    
    monitor = ETLMonitor()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--continuous":
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 15
            monitor.run_continuous_monitoring(interval)
        elif sys.argv[1] == "--check":
            monitor.run_full_check()
    else:
        # Execução única por padrão
        monitor.run_full_check()

