from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd
import sys
import os
import numpy as np
from pathlib import Path

MODEL_PATH = "/opt/airflow/model"

if not os.path.exists(MODEL_PATH):
    MODEL_PATH = str(Path(__file__).resolve().parent.parent / "model")

if MODEL_PATH not in sys.path:
    sys.path.append(MODEL_PATH)

# Now import your module
import fetch_housing_data


import fetch_housing_data
import pipeline
import insert_into_postgredb

fetch_active_listings = fetch_housing_data.fetch_active_listings
housing_data_pipeline = pipeline.housing_data_pipeline
confirmation = insert_into_postgredb.confirmation

os.environ['NO_PROXY'] = '*'

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 3, 23),
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
    python_callable=confirmation,
    dag=dag,
)

fetch_task >> retrain_task >> upload_to_database
