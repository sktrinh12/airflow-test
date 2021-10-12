try:
    from datetime import timedelta
    from airflow import DAG
    from airflow.operators.python_operator import PythonOperator
    from datetime import datetime
    import pandas as pd
    from os import path
    print("All DAG modules are ok ... ")
except Exception as e:
    print("Error {} ".format(e))

print("######" + path.splitext(__file__)[0] + "######")


def first_fx_exec(**context):
    print("first_fx_exec     ")
    context['ti'].xcom_push(key='mykey', value="first_fx_exec says hello")

# ti = task instance
def second_fx_exec(**context):
    instance = context.get("ti").xcom_pull(key="mykey")
    data = [{"name":"Spencer","title":"Scientist"},
            {"name":"Felix","title":"game developer"}]
    df = pd.DataFrame(data=data)
    print('@'*66)
    print(df.head())
    print('@'*66)
    print("I am in second_fx_exec got value: {} from function 1 ".format(instance))
    # var = kwargs.get("name", "no value")
    # msg = "Hello world {}".format(var)
    # print(msg)
    # return msg

# Execute every Two minutes
with DAG(
    dag_id=path.splitext(path.basename(__file__))[0],
    # schedule_interval="*/2 * * * *",
    default_args={
        "owner":"airflow",
        "retries":1,
        "retry_delay":timedelta(minutes=5),
        "start_date":datetime(2020,11,1),
    },
    catchup=False) as dag:

    first_fx_exec = PythonOperator(
        task_id="first_fx_exec",
        python_callable=first_fx_exec,
        provide_context=True,
        op_kwargs={"name":"Spencer Trinh"}
    )

    second_fx_exec = PythonOperator(
        task_id="second_fx_exec",
        python_callable=second_fx_exec,
        provide_context=True
    )

first_fx_exec >> second_fx_exec
