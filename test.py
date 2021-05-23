import requests
import json
from datetime import datetime
from pprint import pprint


headers = {
    'accept':'application/json',
    'content-type':'application/json',
}
auth = ('airflow','airflow')
body = {
    "conf": {},
    "dag_run_id":"testrun08",
    "execution_date":datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
}

result = requests.post(
  "http://localhost:8080/api/v1/dags/r_dag/dagRuns",
    headers=headers,
    auth=auth,
  data=json.dumps(body)
)
pprint(result.content.decode('utf-8'))
