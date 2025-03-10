from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd
import sys
import os
import numpy as np

MODEL_PATH = "/opt/airflow/model"
if MODEL_PATH not in sys.path:
    sys.path.append(MODEL_PATH)

import fetch_housing_data
import pipeline
import insert_into_postgredb

fetch_active_listings = fetch_housing_data.fetch_active_listings
housing_data_pipeline = pipeline.housing_data_pipeline
psql_insert_copy = insert_into_postgredb.psql_insert_copy

os.environ['NO_PROXY'] = '*'

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 3, 10),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "retrain_rental_model",
    default_args=default_args,
    description="Fetch rental listings and retrain model",
    schedule_interval="0 0 */3 * *",  
)

fetch_task = PythonOperator(
    task_id="fetch_active_listings",
    python_callable=fetch_active_listings,
    retries=0, 
    execution_timeout=timedelta(minutes=1),  
    dag=dag,
)

retrain_task = PythonOperator(
    task_id="call_pipeline",
    python_callable=housing_data_pipeline,
    execution_timeout=timedelta(minutes=5),  
    dag=dag,
)

upload_to_database = PythonOperator(
    task_id="upload_to_database",
    python_callable=psql_insert_copy,
    dag=dag,
)

fetch_task >> retrain_task >> upload_to_database
