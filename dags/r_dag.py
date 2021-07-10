import os
from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
print("All DAG modules are ok ... ")

default_args = {
        "owner":"airflow",
        "description":"use of DockerOperator",
        "depends_on_past":False,
        "start_date":datetime.now(),
        "email_on_failure":False,
        "email_on_retry":False,
        "retries":3,
        "retry_delay":timedelta(minutes=5)
    }


with DAG(
    dag_id=os.path.splitext(os.path.basename(__file__))[0],
    default_args=default_args,
    catchup=False) as dag:

    t_bash = BashOperator(
        task_id="bash_output",
        bash_command='echo "today is: $(date)" - {{ dag_run.conf["EXP_ID"] }}'
    )

    t_docker = DockerOperator(
        task_id='docker_command',
        image='bdb/omiq:latest',
        api_version='auto',
        auto_remove=True,
        force_pull=False,
	volumes = ['/datadump:/datadump:z', '/home/ca10322096/scripts:/scripts:z'],
       # command='Rscript -e "print(list.files(file.path(\'/mnt/data/20211506TEST\')))"',
	command='Rscript /scripts/main_driver.R {{ dag_run.conf["EXP_ID"] }}',
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge'
    )

    t_bash >> t_docker
