#!/bin/bash

export AIRFLOW_HOME=$(pwd)/airflow

mkdir .venvs
python3 -m venv .venvs/airflow-env
source .venvs/airflow-env/bin/activate

AIRFLOW_VERSION=2.7.0
PYTHON_VERSION="$(python3 --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

pip install pandas psycopg2-binary

airflow db init
airflow standalone

exit(0)
# airflow users create \\
#     --username admin \\
#     --password admin \\
#     --role Admin \\
#     --firstname admin \\
#     --lastname admin \\
#     --email admin@polytech.com

# postgresql://doadmin:AVNS_J9cM0dX1dTZ2J0vNuAN@db-postgresql-polytech-airflow-do-user-3783411-0.b.db.ondigitalocean.com:25060/kevinl-airflow