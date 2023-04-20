# Main functionality libraries:
from typing import Any
from yaml import safe_load
from os import path

import google.auth
from google.auth.transport.requests import AuthorizedSession
import requests


# Following GCP best practices, these credentials should be
# constructed at start-up time and used throughout
# https://cloud.google.com/apis/docs/client-libraries-best-practices
AUTH_SCOPE = "https://www.googleapis.com/auth/cloud-platform"
CREDENTIALS, _ = google.auth.default(scopes=[AUTH_SCOPE])

def make_composer2_web_server_request(
    url: str, 
    method: str = "GET", 
    **kwargs: Any
) -> google.auth.transport.Response:
    """
    Make a request to Cloud Composer 2 environment's web server.
    Args:
        url: The URL to fetch.
        method: The request method to use ('GET', 'OPTIONS', 'HEAD', 'POST', 'PUT',
        'PATCH', 'DELETE')
        **kwargs: Any of the parameters defined for the request function:
                https://github.com/requests/requests/blob/master/requests/api.py
                If no timeout is provided, it is set to 90 by default.
    """

    authed_session = AuthorizedSession(CREDENTIALS)

    # Set the default timeout, if missing
    if "timeout" not in kwargs:
        kwargs["timeout"] = 90

    return authed_session.request(method, url, **kwargs)

def trigger_dag(
    web_server_url: str, 
    dag_id: str, 
    data: dict
) -> str:
    """
    Make a request to trigger a dag using the stable Airflow 2 REST API.
    https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html

    Args:
        web_server_url: The URL of the Airflow 2 web server.
        dag_id: The DAG ID.
        data: Additional configuration parameters for the DAG run (json).
    """

    endpoint = f"api/v1/dags/{dag_id}/dagRuns"
    request_url = f"{web_server_url}/{endpoint}"
    json_data = {"conf": data}

    response = make_composer2_web_server_request(
        request_url, method="POST", json=json_data
    )


    # if response.status_code == 403:
    #     raise requests.HTTPError(
    #         "You do not have a permission to perform this operation. "
    #         "Check Airflow RBAC roles for your account."
    #         f"{response.headers} / {response.text}"
    #     )
    if response.status_code != 200:
        print(f'HTTP error {response.status_code}, {response.text}')
    # else:
    return response.status_code, response.text

def run(event, context) -> int:
    blob_name = event['name']

    # Read in config data
    base_path = path.dirname(path.abspath(__file__))
    with open(f'{base_path}/config.yaml') as config_data:
        config = safe_load(config_data.read())
        config = config['trigger_dag']

    print(f'Running for {blob_name}')
    
    # We are not using the following sources at the moment, ignoring those files
    ignored_sources = ['DispatchAllocationsProcess', 'Email', 'IVQ', 'PackageLines', 'Stock', 'TablesRowCount']
    if not any(source in blob_name for source in ignored_sources):
        # Create dict to pass to DAG
        file_name = blob_name.split('/')[-1]
        file_stem = file_name.split('.')[0]
        data = {
            'blob_name': blob_name,
            'file_name': file_name,
            'file_stem': file_stem,
            'time_created': event['timeCreated'],
            'source_bucket_name': event['bucket'],
            'target_project_id': config['target_project_id'], 
            'target_dataset': config['target_dataset'], #FIXME: Should maybe not be conf but what's the format?
            'target_table': file_stem,
            'target_bucket': config['target_bucket'], 
        }
        
        req_status, req_text = trigger_dag(
            config['cloud_composer_url'], 
            config['dag_id'], 
            data
        )

        return req_status
    else:
        # Returning fake HTTP response code 204, no content
        return 204
