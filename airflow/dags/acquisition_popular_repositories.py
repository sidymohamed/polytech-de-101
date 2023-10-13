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
    dag_id="acquisition_popular_repositories",
    schedule=None,
    start_date=datetime.datetime(2023,9,1),
    catchup=False,
    tags=["acquisition"],
) as dag:

    @task(task_id="acquisition_popular_repo")
    def acquisition_popular_repo(**kwargs):

        # from https://docs.github.com/fr/rest/search/search?apiVersion=2022-11-28#search-repositories
        github_search_query = "stars:>1000"

        response = run_github_rest_query(endpoint="search/repositories", params={"q": github_search_query, "sort": "stars", "order": "desc"})

        push_data_to_datalake(
            data=json.dumps(response.json()["items"]),
            bucket_name="datalake-polytech-de-101",
            file_key="kevinl/acquisition/repositories/popular_repo_2023_10_10.json"
        )

    acquisition = acquisition_popular_repo()

    @task(task_id="consolidate_popular_repo")
    def consolidate_popular_repo(**kwargs):

        raw_data = pull_data_from_datalake(
            bucket_name="datalake-polytech-de-101",
            file_key="kevinl/acquisition/repositories/popular_repo_2023_10_10.json"
        )

        df = pd.read_json(raw_data, orient="records")
        df = df[[
            "id",
            "name",
            "full_name",
            "description",
            "size",
            "stargazers_count",
            "watchers_count",
            "forks_count",
            "open_issues_count",
            "visibility",
            "html_url",
            "forks_url",
            "commits_url",
            "languages_url",
            "issues_url"
        ]]

        insert_df_in_warehouse(df, "consolidate_repositories", "consolidate", "replace")

    consolidate_data = consolidate_popular_repo()

    acquisition >> consolidate_data
