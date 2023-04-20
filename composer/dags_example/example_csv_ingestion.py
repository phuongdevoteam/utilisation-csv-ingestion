from datetime import datetime, timedelta
import os

from composer_csv_ingestion.csv_ingestion_to_landing_zone import create_csv_ingestion_to_landing_zone_dag
from composer_csv_ingestion.csv_ingestion import create_csv_ingestion_dag

from dags_example.example_csv_ingestion_files.batch_number_calc import (
    bn_func
)


home_folder = os.environ['DAGS_FOLDER'].rsplit('/', 1)[0]
sql_files = os.listdir(f'{home_folder}/dags/example/example_csv_ingestion_files/include/')
sql_files = [ ddl_file.split('.')[0] for ddl_file in sql_files ]

for source in sql_files:
    source_rem_underscore = source.split('_')[1]

    csv_ingestion_dag_name = f'example__{source_rem_underscore}_csv_ingestion'
    landing_zone_dag_name = f'example__{source_rem_underscore}_landing_zone'

    globals()[csv_ingestion_dag_name] = create_csv_ingestion_dag(
        dag_name = csv_ingestion_dag_name,
        dag_description = f"Example CSV Ingestion for {source_rem_underscore}",
        schedule = None,
        owner = "Devoteam - Phuong",
        start_date = datetime(2022, 2, 17),
        tags = ['example','Ingestion', 'CSV', source_rem_underscore],
        retries = 3,
        retry_delay = timedelta(seconds = 30),
        email = ['phuong.anh.nguyen@devoteam.com'],
        sql_path = f'dags_example/example_csv_ingestion_files/include/{source}.sql',
        source = 'oil',
        batch_number_func = bn_func,
        # error_handling_entry = None,
        next_dag = landing_zone_dag_name
    )

    globals()[landing_zone_dag_name] = create_csv_ingestion_to_landing_zone_dag(
        dag_name = landing_zone_dag_name,
        dag_description = 'Brings Example files from staging table to landing zone',
        schedule = None,
        owner = 'Devoteam - Phuong',
        start_date = datetime(2022, 2, 17),
        tags = ['Example', 'Ingestion', 'Landing Zone', source_rem_underscore],
        retries = 3,
        retry_delay = timedelta(seconds = 30),
        email = 'phuong.anh.nguyen@devoteam.com',
        config_file_loc = 'dags/dags_example/example_landing_zone_files/config/example_landing_zone_config.yaml'
    )

