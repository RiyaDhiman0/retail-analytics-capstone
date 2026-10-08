from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
with DAG('retail_analytics_pipeline',start_date=datetime(2026,1,1),schedule='*/5 * * * *',catchup=False,default_args={'retries':1,'retry_delay':timedelta(minutes=1)}) as dag:
    bronze=BashOperator(task_id='bronze',bash_command='python /opt/project/src/transform.py')
    quality=BashOperator(task_id='quality_gate',bash_command='python /opt/project/src/quality_checks.py')
    sla=BashOperator(task_id='sla_monitor',bash_command='python /opt/project/src/sla_monitor.py')
    bronze >> quality >> sla
