from airflow import DAG
from airflow.operators import PythonOperator
import requests
from airflow.operators.email_operator import EmailOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'Airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 1),
    'email': ['yogeshkatreddy@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    # 'pool': 'backfill',
}

dag = DAG(
    dag_id='rest_api',
    # start_date = datetime(2019, 1, 1),
    schedule_interval='0 2 * * *',
    default_args=default_args)

userinfo_url = "http://dummy.restapiexample.com/api/v1/employee/1"


def get_user(**kwargs):
    # r = requests.get(userinfo_url)
    # data = r.json()
    data = {'a': 'b'}
    kwargs['ti'].xcom_push(key='value from pusher 1', value=data)
    return data


def print_data(**kwargs):
    ti = kwargs['ti']
    value = ti.xcom_pull(key=None, task_ids='get_user')
    print(value)


get_user = PythonOperator(
    task_id='get_user',
    # python_callable param points to the function you want to run
    python_callable=get_user,
    # dag param points to the DAG that this task is a part o
    dag=dag,
    provide_context=True)

print_data = PythonOperator(
    task_id='print_data',
    python_callable=print_data,
    dag=dag,
    provide_context=True)

# email = EmailOperator(
# task_id='send_email',
# to='yogesh.veera@in.ibm.com',
# subject='Airflow Alert',
# html_content=""" <h3>Email Test</h3> """,
# dag=dag)

start = DummyOperator(
    task_id='start',
    dag=dag)

stop = DummyOperator(
    task_id='stop',
    dag=dag)

start >> get_user >> print_data >> stop
