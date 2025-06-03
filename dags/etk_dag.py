from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
}

with DAG(
    "dispatcher_quality_etl",
    default_args=default_args,
    description="ETL DAG for Dispatcher Quality",
    schedule_interval="@weekly",
    start_date=datetime(2025, 6, 1),
    catchup=False,
) as dag:
    extract_task = BashOperator(
        task_id="extract", bash_command="python /opt/airflow/etl/extract.py"
    )

    transform_task = BashOperator(
        task_id="transform", bash_command="python /opt/airflow/etl/transform.py"
    )

    load_task = BashOperator(
        task_id="load", bash_command="python /opt/airflow/etl/load.py"
    )

    extract_task >> transform_task >> load_task
