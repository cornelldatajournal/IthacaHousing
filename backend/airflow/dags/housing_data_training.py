from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd
import sys
import os
import numpy as np
BACKEND_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, BACKEND_PATH)
from model.fetch_housing_data import fetch_active_listings
from model.pipeline import housing_data_pipeline
from model.model_training import train_model



from model.fetch_housing_data import fetch_active_listings

os.environ['NO_PROXY'] = '*'

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 2, 16),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "retrain_rental_model",
    default_args=default_args,
    description="Fetch rental listings and retrain model",
    schedule_interval="0 0 * * *",  
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
    python_callable=train_model,
    dag=dag,
)

fetch_task >> retrain_task >> upload_to_database
