import logging
from airflow.models import Variable

def run_github_graphql_query(data, graphql_input_variables={}):
    import requests

    headers = {"Authorization": f"token {Variable.get('github_token')}"}

    url = 'https://api.github.com/graphql'

    request_data = {
        "query": data,
        "variables": graphql_input_variables
    }

    try:
        response = requests.post(url=url, data=request_data, headers=headers)
    except Exception as e:
        logging.error("An error occured during the acquisition.")
        raise e
        #doing more stuff is necessary
    finally:
        return response


def run_github_rest_query(endpoint, params={}):
    import requests

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {Variable.get('github_token')}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    url = f"https://api.github.com/{endpoint}"

    try:
        response = requests.get(url=url, params=params, headers=headers)
    except Exception as e:
        raise e
        #doing more stuff is necessary
    finally:
        return response
    

def push_data_to_datalake(data: str, bucket_name: str, file_key: str) -> None:
    import boto3
    import botocore

    session = boto3.session.Session()
    client = session.client(
        's3',
        endpoint_url=Variable.get("datalake_endpoint"),
        config=botocore.config.Config(s3={'addressing_style': 'virtual'}),
        region_name='nyc3',
        aws_access_key_id=Variable.get("datalake_access_key"),
        aws_secret_access_key=Variable.get("datalake_secret_token")
    )

    # Step 3: Call the put_object command and specify the file to upload.
    client.put_object(Bucket=bucket_name, # The path to the directory you want to upload the object to, starting with your Space name.
        Key=file_key, # Object key, referenced whenever you want to access this file later.
        Body=data.encode('utf-8'), # The object's contents.
        ACL='public-read', # Defines Access-control List (ACL) permissions, such as private or public.
    )

def pull_data_from_datalake(bucket_name: str, file_key: str) -> str:
    import boto3
    import botocore

    session = boto3.session.Session()
    client = session.client(
        's3',
        endpoint_url=Variable.get("datalake_endpoint"),
        config=botocore.config.Config(s3={'addressing_style': 'virtual'}),
        region_name='nyc3',
        aws_access_key_id=Variable.get("datalake_access_key"),
        aws_secret_access_key=Variable.get("datalake_secret_token")
    )

    response = client.get_object(Bucket=bucket_name, Key=file_key)
    return response["Body"].read().decode("utf-8")


def execute_query_on_warehouse(sql_query: str):

    from sqlalchemy.engine import URL
    from sqlalchemy import create_engine
    
    url = URL.create(
        "postgresql",
        username=Variable.get("warehouse_username"),
        password=Variable.get("warehouse_password"),  # plain (unescaped) text
        host=Variable.get("warehouse_host"),
        database=Variable.get("warehouse_database"),
        port=Variable.get("warehouse_port")
    )

    engine = create_engine(url)

    with engine.connect() as conn:
        conn.execute(sql_query)


def insert_df_in_warehouse(df, table_name: str, schema_name: str, if_exists: str):

    from sqlalchemy.engine import URL
    from sqlalchemy import create_engine

    url = URL.create(
        "postgresql",
        username=Variable.get("warehouse_username"),
        password=Variable.get("warehouse_password"),  # plain (unescaped) text
        host=Variable.get("warehouse_host"),
        database=Variable.get("warehouse_database"),
        port=Variable.get("warehouse_port")
    )

    engine = create_engine(url)

    with engine.connect() as conn:
        df.to_sql(table_name, conn, schema=schema_name, if_exists=if_exists)
