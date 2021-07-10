# AIRFLOW-TEST

#### Note:

use of the `Dockerfile` requires puckel's rendition of the airflow container at
version 1.10. The current airflow container that was tested uses the newest
version, 2.1.0. However, there is a pending issue with `DockerOperator` where it
does not automatically pull an image if it doesn't exist, therefore pulling
manually prior to or setting `force_pull` to `True` is the only work-around.
