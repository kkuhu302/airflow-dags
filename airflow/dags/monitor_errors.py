from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to operate!
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2020, 8, 13),
    "email": ["kuhu.kuhu@soprasteria.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "catchup": False,
}

dag = DAG("monitor_errors", default_args=default_args, schedule_interval=timedelta(1))



log_list = ['securityApp.log', 'mainApp.log', 'extApp.log', 'timeApp.log', 'tokenApp.log',
            'bridgeApp.log', 'daemonApp.log', 'notificationApp.log', 'messageApp.log']

dl_tasks = []
for file in log_list:
    op = SFTPOperator(task_id=f"download_{file}",
                ssh_conn_id="log_server",
                local_filepath=f"{base_folder}/{file}",
                remote_filepath=f"{remote_path}/{file}",
                operation=SFTPOperation.GET,
                create_intermediate_dirs=True,
                dag=dag)
    dl_tasks.append(op)
