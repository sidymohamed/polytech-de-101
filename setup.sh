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
