\# 🚀 Pipeline de Dados — DncInsight Solutions



Pipeline de dados construído com \*\*Apache Airflow\*\* e \*\*Docker\*\*, processando dados brutos em três camadas: Bronze, Prata e Ouro.



---



\## 📋 Sobre o Projeto



Desenvolvimento de um pipeline automatizado para a empresa DncInsight Solutions, transformando dados brutos em insights estratégicos através de um processo de limpeza, agregação e análise de dados.



---



\## 🏗️ Arquitetura

```

raw\_data.csv

&nbsp;    │

&nbsp;    ▼

┌─────────────────────┐

│  🥉 Camada Bronze    │  Ingestão do dado bruto sem alterações

└──────────┬──────────┘

&nbsp;          │

&nbsp;          ▼

┌─────────────────────┐

│  🥈 Camada Prata     │  Limpeza, validação e cálculo de idade

└──────────┬──────────┘

&nbsp;          │

&nbsp;          ▼

┌─────────────────────┐

│  🥇 Camada Ouro      │  Agregação por faixa etária e status

└─────────────────────┘

```



---



\## 🛠️ Tecnologias Utilizadas



\- \*\*Python 3.8+\*\*

\- \*\*Apache Airflow 2.8.1\*\* — orquestração do pipeline

\- \*\*Docker + Docker Compose\*\* — ambiente isolado e reproduzível

\- \*\*Pandas\*\* — processamento e transformação de dados

\- \*\*PostgreSQL\*\* — banco de dados do Airflow



---



\## 📁 Estrutura do Projeto

```

projeto\_dncinsight/

│

├── dags/

│   └── pipeline\_dncinsight.py   # DAG principal do Airflow

│

├── data/

│   ├── raw\_data.csv             # Arquivo de entrada

│   ├── bronze/                  # Dados brutos copiados

│   ├── prata/                   # Dados limpos + idade calculada

│   └── ouro/                    # Dados agregados prontos para análise

│

├── logs/                        # Logs do Airflow

├── plugins/                     # Plugins extras

├── docker-compose.yml           # Configuração do ambiente Docker

└── README.md

```



---



\## ⚙️ Como Executar



\### Pré-requisitos

\- \[Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e rodando



\### 1. Clonar o repositório

```bash

git clone https://github.com/SEU\_USUARIO/projeto\_dncinsight.git

cd projeto\_dncinsight

```



\### 2. Adicionar o arquivo de dados

Coloque o arquivo `raw\_data.csv` dentro da pasta `data/`



\### 3. Subir o ambiente

```bash

docker compose up -d

```



\### 4. Acessar o Airflow

Abra o navegador em `http://localhost:8080`

\- \*\*Login:\*\* airflow

\- \*\*Senha:\*\* airflow



\### 5. Executar o pipeline

\- Ative o DAG `pipeline\_dncinsight`

\- Clique em ▶ para disparar a execução

\- Acompanhe as tasks em tempo real no Graph View



---



\## 🔄 Etapas do Pipeline



\### 🥉 Bronze — `upload\_raw\_data\_to\_bronze()`

\- Lê o arquivo `raw\_data.csv`

\- Salva na camada Bronze \*\*sem nenhuma alteração\*\*

\- Garante preservação do dado original



\### 🥈 Prata — `process\_bronze\_to\_silver()`

\- Remove registros com campos nulos (`name`, `email`, `date\_of\_birth`)

\- Filtra e-mails inválidos (sem o caractere `@`)

\- Converte `date\_of\_birth` para datetime

\- Calcula a \*\*idade\*\* de cada usuário



\### 🥇 Ouro — `process\_silver\_to\_gold()`

\- Cria a coluna \*\*faixa etária\*\* (0-10, 11-20, 21-30, 31-40, 41-50, 51+)

\- Padroniza a coluna `subscription\_status`

\- Gera agregação por faixa etária e status

\- Salva dois arquivos:

&nbsp; - `users\_enriched.csv` — dataset completo enriquecido

&nbsp; - `users\_by\_age\_and\_status.csv` — tabela agregada para análise



---



\## 📊 Resultados



Após a execução do pipeline os seguintes arquivos são gerados:



| Arquivo | Camada | Descrição |

|---|---|---|

| `bronze/raw\_data.csv` | Bronze | Dado bruto original |

| `prata/clean\_data.csv` | Prata | Dados limpos com idade calculada |

| `ouro/users\_enriched.csv` | Ouro | Dataset completo com faixa etária |

| `ouro/users\_by\_age\_and\_status.csv` | Ouro | Agregação para análise estratégica |



---



\## 🛑 Comandos Úteis

```bash

\# Iniciar

docker compose up -d



\# Parar

docker compose down



\# Ver logs

docker compose logs -f airflow-scheduler



\# Reiniciar scheduler

docker compose restart airflow-scheduler

```

