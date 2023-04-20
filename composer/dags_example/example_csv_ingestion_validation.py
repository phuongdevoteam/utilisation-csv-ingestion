from airflow import DAG
from datetime import datetime, timedelta

from composer_csv_ingestion.csv_ingestion_validation import create_csv_ingestion_validation_dag

from dags_example.example_csv_ingestion_validation_files.collection_creation_func import collection_creation_func
from dags_example.example_csv_ingestion_validation_files.gcs_prefix_creation_func import gcs_prefix_creation_func


dag_name = 'example_ingestion_validation'
globals()[dag_name] = create_csv_ingestion_validation_dag(
    dag_name = dag_name,
    dag_description = "Ingestion validation for example",
    schedule = None,
    owner = 'Devoteam - Phuong',
    start_date = datetime(2022, 2, 17),
    tags = ['example', 'Ingestion', 'Pre-validation'],
    retries = 0,
    retry_delay = timedelta(minutes = 30),
    email = 'phuong.anh.nguyen@devoteam.com',
    collection_creation_func=collection_creation_func,
    gcs_prefix_creation_func=gcs_prefix_creation_func
)