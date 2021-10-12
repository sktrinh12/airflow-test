import os
from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
        "owner":"airflow",
        "description":"automated omiq testing",
        "depends_on_past":False,
        "start_date":datetime.now(),
        "email_on_failure":True,
        "email_on_retry":True,
	"email":["spencer.trinh@bd.com","kristina.shahtatit@bd.com"],
        "retries":3,
        "retry_delay":timedelta(minutes=3)
    }

fp = "/opt/airflow/datadump/data/"
exp_ids = [eid for eid in os.listdir(fp) if os.path.isdir(os.path.join(fp, eid)) and eid.endswith("LWB5")]

with DAG(dag_id=f"{os.path.splitext(os.path.basename(__file__))[0]}_atm_test",
    default_args=default_args,
    catchup=False) as dag:

        previous_t_bash = None
        for eid in exp_ids:
                t_bash = BashOperator(
                task_id="bash_output_%s" % eid,
                bash_command=f'echo "Automation test on: $(date) - { eid }"'
                )

                t_docker = DockerOperator(
                task_id='omiq_pipeline_%s' % eid,
                image='bdb/omiq:1.5.1',
                api_version='auto',
                auto_remove=True,
                force_pull=False,
                volumes = ['/datadump:/datadump:z', '/home/ca10322096/scripts:/scripts:z'],
                command=f'Rscript /scripts/main_driver.R { eid } false',
                docker_url='unix://var/run/docker.sock',
                network_mode='bridge'
                )
                if previous_t_bash:
                        previous_t_bash >> t_bash
                t_bash >> t_docker
                previous_t_bash = t_docker
