#!/bin/bash
set -e  

echo "Starting Airflow Setup..."

if [ ! -f /airflow_initialized ]; then
    echo "Initializing Airflow DB..."
    airflow db init && airflow db upgrade
    touch /opt/airflow/airflow_initialized
else
    echo "Airflow DB already initialized. Skipping db init."
fi

airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email asmaitra2006@gmail.com || true

airflow scheduler & exec airflow webserver
