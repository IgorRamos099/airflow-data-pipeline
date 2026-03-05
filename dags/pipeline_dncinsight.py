from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import os
import re

# ── Caminhos das camadas ─────────────────────────────────────────────────────
BASE_PATH   = '/opt/airflow/data'
BRONZE_PATH = os.path.join(BASE_PATH, 'bronze')
PRATA_PATH  = os.path.join(BASE_PATH, 'prata')
OURO_PATH   = os.path.join(BASE_PATH, 'ouro')
RAW_FILE    = os.path.join(BASE_PATH, 'raw_data.csv')


# ── TASK 1: Camada Bronze ────────────────────────────────────────────────────
def upload_raw_data_to_bronze():
    os.makedirs(BRONZE_PATH, exist_ok=True)

    if not os.path.exists(RAW_FILE):
        raise FileNotFoundError(f'raw_data.csv nao encontrado em: {RAW_FILE}')

    df = pd.read_csv(RAW_FILE)
    print(f'[BRONZE] Registros carregados: {len(df)}')
    print(f'[BRONZE] Colunas: {list(df.columns)}')

    output = os.path.join(BRONZE_PATH, 'raw_data.csv')
    df.to_csv(output, index=False)
    print(f'[BRONZE] Salvo em: {output}')


# ── TASK 2: Camada Prata ─────────────────────────────────────────────────────
def process_bronze_to_silver():
    os.makedirs(PRATA_PATH, exist_ok=True)

    df = pd.read_csv(os.path.join(BRONZE_PATH, 'raw_data.csv'))
    total_inicial = len(df)
    print(f'[PRATA] Recebidos da Bronze: {total_inicial}')

    # 1. Remover nulos em campos criticos
    colunas_criticas = [c for c in ['name', 'email', 'date_of_birth'] if c in df.columns]
    df = df.dropna(subset=colunas_criticas)
    print(f'[PRATA] Apos remover nulos: {len(df)}')

    # 2. Filtrar emails invalidos (precisam ter @)
    if 'email' in df.columns:
        email_valido = lambda e: isinstance(e, str) and bool(re.search(r'@', e))
        df = df[df['email'].apply(email_valido)]
        print(f'[PRATA] Apos filtrar emails invalidos: {len(df)}')

    # 3. Calcular idade a partir da data de nascimento
    if 'date_of_birth' in df.columns:
        df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], errors='coerce')
        df = df.dropna(subset=['date_of_birth'])
        hoje = pd.Timestamp.today()
        df['idade'] = df['date_of_birth'].apply(lambda d: (hoje - d).days // 365)
        print(f'[PRATA] Coluna idade calculada. Min: {df["idade"].min()}, Max: {df["idade"].max()}')

    print(f'[PRATA] Total removido: {total_inicial - len(df)} | Salvo: {len(df)}')
    df.to_csv(os.path.join(PRATA_PATH, 'clean_data.csv'), index=False)


# ── TASK 3: Camada Ouro ──────────────────────────────────────────────────────
def process_silver_to_gold():
    os.makedirs(OURO_PATH, exist_ok=True)

    df = pd.read_csv(os.path.join(PRATA_PATH, 'clean_data.csv'))
    print(f'[OURO] Recebidos da Prata: {len(df)}')
    print(f'[OURO] Colunas: {list(df.columns)}')

    def faixa_etaria(idade):
        if   idade <= 10: return '0 a 10'
        elif idade <= 20: return '11 a 20'
        elif idade <= 30: return '21 a 30'
        elif idade <= 40: return '31 a 40'
        elif idade <= 50: return '41 a 50'
        else:             return '51+'

    df['faixa_etaria'] = df['idade'].apply(faixa_etaria)

    if 'subscription_status' in df.columns:
        df['subscription_status'] = df['subscription_status'].str.strip().str.lower()

    agg_df = (
        df.groupby(['faixa_etaria', 'subscription_status'], as_index=False)
          .agg(total_usuarios=('name', 'count'))
          .sort_values(['faixa_etaria', 'subscription_status'])
    )

    print('[OURO] Agregacao por faixa etaria e status:')
    print(agg_df.to_string(index=False))

    df.to_csv(os.path.join(OURO_PATH, 'users_enriched.csv'), index=False)
    agg_df.to_csv(os.path.join(OURO_PATH, 'users_by_age_and_status.csv'), index=False)
    print('[OURO] Arquivos salvos com sucesso!')


# ── Definicao do DAG ─────────────────────────────────────────────────────────
default_args = {
    'owner': 'dncinsight',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='pipeline_dncinsight',
    default_args=default_args,
    description='Pipeline Bronze -> Prata -> Ouro — DncInsight Solutions',
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['dncinsight', 'data-pipeline'],
) as dag:

    t1_bronze = PythonOperator(
        task_id='upload_raw_data_to_bronze',
        python_callable=upload_raw_data_to_bronze,
    )

    t2_prata = PythonOperator(
        task_id='process_bronze_to_silver',
        python_callable=process_bronze_to_silver,
    )

    t3_ouro = PythonOperator(
        task_id='process_silver_to_gold',
        python_callable=process_silver_to_gold,
    )

    t1_bronze >> t2_prata >> t3_ouro