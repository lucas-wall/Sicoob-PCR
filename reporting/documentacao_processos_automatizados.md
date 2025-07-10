# Documentação dos Processos Automatizados - ETL SICOOB

## Visão Geral

Este documento descreve os processos automatizados implementados para o pipeline ETL (Extract, Transform, Load) do Dashboard de Crédito Rural do SICOOB. O sistema foi projetado para executar de forma autônoma, com monitoramento contínuo e alertas automáticos.

## Arquitetura do Sistema

### Componentes Principais

1. **Script de Extração** (`script_extracao_dados.py`)
2. **Script de Transformação** (`script_transformacao_dados.py`)
3. **Script de Carregamento** (`script_carregamento_powerbi.py`)
4. **Agendador** (`agendamento_scripts.py`)
5. **Monitor** (`monitoramento_alertas.py`)

### Fluxo de Dados

```
[Sistema SICOOB] → [Extração] → [Transformação] → [Carregamento] → [Power BI]
                      ↓              ↓              ↓
                 [Monitoramento] [Monitoramento] [Monitoramento]
                      ↓              ↓              ↓
                   [Alertas]      [Alertas]      [Alertas]
```

## Processos Automatizados

### 1. Pipeline ETL Principal

#### 1.1 Extração de Dados
- **Arquivo**: `script_extracao_dados.py`
- **Função**: Extrai dados do sistema SICOOB
- **Frequência**: Diária às 06:00 e segunda-feira às 08:00
- **Timeout**: 5 minutos
- **Saídas**:
  - `dados_carteira_extraidos.csv`
  - `dados_clientes_extraidos.csv`
  - `dados_cooperativas_extraidos.csv`

#### 1.2 Transformação de Dados
- **Arquivo**: `script_transformacao_dados.py`
- **Função**: Limpa e transforma os dados extraídos
- **Dependência**: Extração concluída
- **Timeout**: 5 minutos
- **Saídas**:
  - `fact_credito_rural.csv`
  - `dim_tempo.csv`
  - `dim_linha_credito.csv`
  - `dim_cultura.csv`
  - `dim_cooperativas.csv`

#### 1.3 Carregamento para Power BI
- **Arquivo**: `script_carregamento_powerbi.py`
- **Função**: Prepara dados para o Power BI
- **Dependência**: Transformação concluída
- **Timeout**: 5 minutos
- **Saídas**:
  - Arquivos CSV e Parquet otimizados
  - Medidas DAX
  - Documentação do modelo

### 2. Sistema de Agendamento

#### 2.1 Configuração de Horários
- **Execução Principal**: Diária às 06:00
- **Execução Semanal**: Segunda-feira às 08:00
- **Verificação de Saúde**: A cada 4 horas

#### 2.2 Funcionalidades
- Execução sequencial dos scripts ETL
- Controle de timeout para cada etapa
- Notificação por email em caso de sucesso/falha
- Log detalhado de todas as operações

#### 2.3 Comandos
```bash
# Execução manual
python3.11 agendamento_scripts.py --manual

# Execução agendada (modo daemon)
python3.11 agendamento_scripts.py
```

### 3. Sistema de Monitoramento

#### 3.1 Métricas Monitoradas

##### Recursos do Sistema
- **Uso de Disco**: Alerta em 80%, crítico em 90%
- **Uso de Memória**: Alerta em 80%, crítico em 90%
- **Uso de CPU**: Alerta em 80%, crítico em 90%

##### Integridade de Arquivos
- Existência dos arquivos obrigatórios
- Idade dos arquivos (alerta se > 25 horas)
- Tamanho dos arquivos (crítico se vazio)

##### Análise de Logs
- Detecção de erros nos logs
- Contagem de erros recentes
- Alertas baseados na frequência de erros

#### 3.2 Níveis de Alerta
- **INFO**: Informações gerais
- **WARNING**: Situações que requerem atenção
- **CRITICAL**: Problemas que impedem o funcionamento

#### 3.3 Comandos
```bash
# Verificação única
python3.11 monitoramento_alertas.py --check

# Monitoramento contínuo (15 minutos)
python3.11 monitoramento_alertas.py --continuous

# Monitoramento contínuo (intervalo personalizado)
python3.11 monitoramento_alertas.py --continuous 30
```

## Configurações

### 1. Configuração de Email

#### Arquivo: `monitoring_config.json`
```json
{
  "email": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "email_user": "monitoring@sicoob.com.br",
    "email_password": "senha_app",
    "recipients": ["ti@sicoob.com.br", "gestao@sicoob.com.br"]
  }
}
```

### 2. Thresholds de Monitoramento

```json
{
  "thresholds": {
    "disk_usage_warning": 80,
    "disk_usage_critical": 90,
    "memory_usage_warning": 80,
    "memory_usage_critical": 90,
    "cpu_usage_warning": 80,
    "cpu_usage_critical": 90,
    "etl_timeout_minutes": 30,
    "file_age_hours": 25
  }
}
```

## Logs e Auditoria

### 1. Arquivos de Log

- **`etl_log.log`**: Logs do pipeline ETL
- **`scheduler_log.log`**: Logs do agendador
- **`monitoring_log.log`**: Logs do monitoramento

### 2. Arquivo de Status

- **`etl_status.json`**: Status atual do sistema
- Atualizado a cada verificação
- Contém informações sobre saúde do sistema

### 3. Retenção de Logs

- Logs são mantidos por 30 dias
- Rotação automática quando atingem 10MB
- Backup diário dos logs críticos

## Procedimentos de Manutenção

### 1. Verificação Diária

1. Verificar execução do pipeline ETL
2. Revisar logs de erro
3. Confirmar atualização dos dados no Power BI
4. Verificar alertas recebidos

### 2. Verificação Semanal

1. Análise de performance do sistema
2. Revisão de thresholds de monitoramento
3. Limpeza de arquivos temporários
4. Backup dos dados críticos

### 3. Verificação Mensal

1. Análise de tendências de performance
2. Otimização de queries e transformações
3. Atualização de dependências
4. Revisão da documentação

## Troubleshooting

### 1. Falhas Comuns

#### Pipeline ETL Falha
1. Verificar conectividade com banco de dados
2. Verificar espaço em disco
3. Verificar logs de erro específicos
4. Executar pipeline manualmente para debug

#### Alertas Não Enviados
1. Verificar configuração de email
2. Verificar conectividade de rede
3. Verificar credenciais de email
4. Testar envio manual

#### Dados Desatualizados
1. Verificar execução do agendador
2. Verificar logs do pipeline ETL
3. Verificar integridade dos arquivos fonte
4. Executar pipeline manual

### 2. Comandos de Diagnóstico

```bash
# Verificar status do sistema
python3.11 monitoramento_alertas.py --check

# Executar pipeline manual
python3.11 agendamento_scripts.py --manual

# Verificar logs
tail -f etl_log.log
tail -f scheduler_log.log
tail -f monitoring_log.log

# Verificar arquivos de dados
ls -la *.csv
ls -la powerbi_data/
```

## Contatos e Suporte

### Equipe Responsável
- **TI SICOOB**: ti@sicoob.com.br
- **Gestão de Dados**: gestao@sicoob.com.br
- **Suporte 24/7**: suporte@sicoob.com.br

### Escalação
1. **Nível 1**: Analista de TI
2. **Nível 2**: Coordenador de TI
3. **Nível 3**: Gerente de TI

## Versionamento

- **Versão**: 1.0
- **Data de Criação**: 09/07/2025
- **Última Atualização**: 09/07/2025
- **Próxima Revisão**: 09/08/2025

## Anexos

### A. Estrutura de Diretórios

```
/home/ubuntu/
├── script_extracao_dados.py
├── script_transformacao_dados.py
├── script_carregamento_powerbi.py
├── agendamento_scripts.py
├── monitoramento_alertas.py
├── dados_carteira_extraidos.csv
├── dados_clientes_extraidos.csv
├── dados_cooperativas_extraidos.csv
├── fact_credito_rural.csv
├── dim_*.csv
├── powerbi_data/
│   ├── fact_credito_rural.csv
│   ├── fact_credito_rural.parquet
│   ├── dim_*.csv
│   ├── dim_*.parquet
│   ├── medidas_dax.json
│   ├── documentacao_modelo.json
│   └── refresh_dashboard.py
├── etl_log.log
├── scheduler_log.log
├── monitoring_log.log
├── monitoring_config.json
└── etl_status.json
```

### B. Dependências do Sistema

```
Python 3.11+
pandas
numpy
sqlite3
schedule
psutil
pyarrow
logging
smtplib
```

### C. Comandos de Instalação

```bash
pip3 install pandas numpy schedule psutil pyarrow
```

