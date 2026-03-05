# Pipeline de Dados 



Pipeline de dados construído com Apache Airflow e Docker, processando dados brutos em três camadas: Bronze, Prata e Ouro.



---



## Sobre o Projeto



Desenvolvimento de um pipeline automatizado, transformando dados brutos em insights estratégicos através de um processo de limpeza, agregação e análise de dados.



---

##  Tecnologias Utilizadas



- **Python 3.8+**

- **Apache Airflow 2.8.1** — orquestração do pipeline

- **Docker + Docker Compose** — ambiente isolado e reproduzível

- **Pandas** — processamento e transformação de dados

- **PostgreSQL** — banco de dados do Airflow



---



## Estrutura do Projeto

```

projeto_dncinsight/

│

├── dags/

│   └── pipeline\_dncinsight.py   # DAG principal do Airflow

│

├── data/

│   ├── raw_data.csv             # Arquivo de entrada

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



##  Como Executar



### Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e rodando



### 1. Clonar o repositório

```bash

git clone https://github.com/SEU_USUARIO/projeto\_dncinsight.git

cd projeto\_dncinsight

```



### 2. Adicionar o arquivo de dados

Coloque o arquivo `raw_data.csv` dentro da pasta `data/`



### 3. Subir o ambiente

```bash

docker compose up -d

```



### 4. Acessar o Airflow

Abra o navegador em `http://localhost:8080`

- Login: airflow

- Senha: airflow



### 5. Executar o pipeline

- Ative o DAG `pipeline_dncinsight`

- Clique em start para disparar a execução

- Acompanhe as tasks em tempo real no Graph View



---



## 🔄 Etapas do Pipeline



### 🥉 Bronze — `upload_raw_data_to_bronze()`

- Lê o arquivo `raw_data.csv`

- Salva na camada Bronze sem nenhuma alteração

- Garante preservação do dado original



### 🥈 Prata — `process_bronze_to_silver()`

- Remove registros com campos nulos (`name`, `email`, `date_of_birth`)

- Filtra e-mails inválidos (sem o caractere `@`)

- Converte `date_of_birth` para datetime

- Calcula a idade de cada usuário



### 🥇 Ouro — `process_silver_to_gold()`

- Cria a coluna faixa etária (0-10, 11-20, 21-30, 31-40, 41-50, 51+)

- Padroniza a coluna `subscription_status`

- Gera agregação por faixa etária e status

- Salva dois arquivos:

- `users_enriched.csv` — dataset completo enriquecido

- `users_by_age_and_status.csv` — tabela agregada para análise



---



## 📊 Resultados



Após a execução do pipeline os seguintes arquivos são gerados:



| Arquivo | Camada | Descrição |

|---|---|---|

| `bronze_raw_data.csv` | Bronze | Dado bruto original |

| `prata/clean_data.csv` | Prata | Dados limpos com idade calculada |

| `ouro/users_enriched.csv` | Ouro | Dataset completo com faixa etária |

| `ouro/users_by_age_and_status.csv` | Ouro | Agregação para análise estratégica |



---



## 🛑 Comandos Úteis

```bash

# Iniciar

docker compose up -d



# Parar

docker compose down



# Ver logs

docker compose logs -f airflow-scheduler



# Reiniciar scheduler

docker compose restart airflow-scheduler

```

