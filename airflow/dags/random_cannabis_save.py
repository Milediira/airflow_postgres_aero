from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime
from random_cannabis_operator import RandomCannabisOperator

doc_md = """
#### Тестовое задание Aero DE.
Автор: Ирина Бабинцева
"""

DEFAULT_ARGS = {
    'owner': 'babintseva',
    'provide_context': True
}

with DAG(
    dag_id='random_cannabis_save',
    default_args=DEFAULT_ARGS,
    start_date=datetime(year=2023, month=9, day=4),
    schedule_interval='0 */12 * * *',
    catchup=False,
    tags=['random_cannabis', 'babintseva'],
    max_active_runs=1,
    doc_md=doc_md
) as dag:

    start = DummyOperator(task_id='start')
    finish = DummyOperator(task_id='finish')

    get_random_cannabis = RandomCannabisOperator(
        task_id='get_random_cannabis',
        size=10
    )

start >> get_random_cannabis >> finish
