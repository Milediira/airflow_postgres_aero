import logging
import requests
from airflow.models import BaseOperator
import dataset
import os

class RandomCannabisOperator(BaseOperator):
    api_url = 'https://random-data-api.com/api/cannabis/random_cannabis'
    template_fields = ("size")

    def __init__(self, size: int = 10, **kwargs) -> None:
        super().__init__(**kwargs)
        self.size = size

    def save_data(self, df: dict):
        uri = os.getenv("AIRFLOW_CONN_DWH_DB")
        db = dataset.connect(uri)
        db.begin()
        try:
            table = db['random_cannabis']
            table.insert_many(rows=df, chunk_size=10000)
            db.commit()
        except Exception as e:
            db.rollback()

    def execute(self, context):
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json;charset=UTF-8'
        }
        response = requests.get(f'{self.api_url}?size={self.size}', headers=headers)
        if response.status_code == 200:
            data = response.json()
            self.save_data(data)
        else:
            logging.error(f"Request failed with status code: {response.status_code}")


