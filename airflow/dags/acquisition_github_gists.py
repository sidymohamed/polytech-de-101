#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
Example DAG demonstrating the usage of the TaskFlow API to execute Python functions natively and within a
virtual environment.
"""
import json
import datetime

import pandas as pd
from airflow import DAG
from airflow.decorators import task

from utils import (
    run_github_rest_query, 
    push_data_to_datalake, 
    pull_data_from_datalake,
    insert_df_in_warehouse 
)


with DAG(
    dag_id="acquisition_github_gists",
    schedule=None,
    start_date=datetime.datetime(2023,9,1),
    catchup=False,
    tags=["example"],
) as dag:

    @task(task_id="acquisition_gists")
    def acquisition_gists(**kwargs):
        response = run_github_rest_query(endpoint="gists/public")

        push_data_to_datalake(data=json.dumps(response.json()), bucket_name="datalake-polytech-de-101", file_key="kevinl/acquisition/gists/gists_2023_10_10.json")

    acquisition_gists = acquisition_gists()
    
    # [START howto_operator_python]
    @task(task_id="consolidate_gists")
    def consolidate_gists(**kwargs):

        raw_data = pull_data_from_datalake(
            bucket_name="datalake-polytech-de-101",
            file_key="kevinl/acquisition/gists/gists_2023_10_10.json"
        )

        df = pd.read_json(raw_data, orient="records")
        df = df[["url","forks_url","commits_url","id","node_id","public","created_at","updated_at","description","comments","user","comments_url","truncated"]]

        insert_df_in_warehouse(df, "consolidate_gists", "consolidate", "replace")

    consolidate_data = consolidate_gists()

    acquisition_gists >> consolidate_data