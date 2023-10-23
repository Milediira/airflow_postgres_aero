from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime
from nhl_stats_save_operator import NhlStatsSaveOperator

doc_md = """
#### Тестовое задание Aero DE.
Автор: Ирина Бабинцева
"""

DEFAULT_ARGS = {
    'owner': 'babintseva',
    'provide_context': True
}

with DAG(
    dag_id='nhl_stats_save',
    default_args=DEFAULT_ARGS,
    start_date=datetime(year=2023, month=9, day=4),
    schedule_interval='0 */12 * * *',
    catchup=False,
    tags=['nhl', 'babintseva'],
    max_active_runs=1,
    doc_md=doc_md
) as dag:

    start = DummyOperator(task_id='start')
    finish = DummyOperator(task_id='finish')

    save_nhl_stats = NhlStatsSaveOperator(
        task_id='save_nhl_stats',
        team_id=21
    )

start >> save_nhl_stats >> finish
