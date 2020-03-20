from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

def export_events():
    return 'export_events'

def train_model():
    return 'train_model'

def upload_predictions():
    return 'upload_predictions'

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2018, 12, 1, 10, 00, 00),
    'concurrency': 1,
    'retries': 1
}

# define the DAG
dag = DAG('train_model', catchup=False, default_args=default_args, schedule_interval=timedelta(seconds=300))

# define the operations
opr_export_events = PythonOperator(task_id='export_events', python_callable=export_events, dag=dag)

opr_train_model = PythonOperator(task_id='train_model', python_callable=train_model, dag=dag)

opr_upload_predictions = PythonOperator(task_id='upload_predictions', python_callable=upload_predictions, dag=dag)

# link operations
opr_export_events >> opr_train_model >> opr_upload_predictions
