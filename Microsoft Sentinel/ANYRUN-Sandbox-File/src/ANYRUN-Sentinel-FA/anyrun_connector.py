import logging as log
import traceback
from json import dumps

import azure.functions as func
from azure.storage.blob import BlobServiceClient
from anyrun.connectors import SandboxConnector
from anyrun.connectors.sandbox.base_connector import BaseSandboxConnector
from anyrun import RunTimeException

from .config import Config


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        log.info('AnyRunDefender started. Checking ANY.RUN Sandbox credentials...')
        token = req.params.get('token') or req.get_json().get('token')

        with BaseSandboxConnector(api_key=token, integration=Config.VERSION) as connector:
            connector.check_authorization()
            log.info('Successful credentials check.')

        filename =  req.params.get('filename') or req.get_json().get('filename')
        blob_container_name = req.params.get('blob_container_name') or req.get_json().get('blob_container_name')
        azure_conn_string = req.params.get('azure_conn_string') or req.get_json().get('azure_conn_string')
        environment = req.params.get('environment') or req.get_json().get('environment')
        analysis_options = req.params.get('analysis_options') or req.get_json().get('analysis_options')

        file = download_file_from_storage(filename, blob_container_name, azure_conn_string)

        if environment == 'windows':
            with SandboxConnector.windows(api_key=token, integration=Config.VERSION) as connector:
                task_uuid = connector.run_file_analysis(
                    file_content=file, filename=filename, **analysis_options
                )
        elif environment == 'linux':
            with SandboxConnector.linux(api_key=token, integration=Config.VERSION) as connector:
                task_uuid = connector.run_file_analysis(
                    file_content=file, filename=filename, **analysis_options
                )

        return func.HttpResponse(
            dumps({'data': {'taskid': task_uuid}}),
            status_code=200,
        )


    except RunTimeException as error:
        return func.HttpResponse(str(error), status_code=500)
    except Exception:
        error_msg = traceback.format_exc()
        log.error(f'Unspecified exception occurred: {error_msg}')
        log.error(error_msg)
        return func.HttpResponse(f'Unspecified exception: {error_msg}', status_code=500)


def download_file_from_storage(filename: str, blob_container_name: str, azure_conn_string: str) -> bytes | None:
    """
    Downloads file from the BlobStorage

    :param filename: Filename
    :return: File content
    """
    blob_service_client = BlobServiceClient.from_connection_string(azure_conn_string)
    container_client = blob_service_client.get_container_client(blob_container_name)

    try:
        file_data = container_client.get_blob_client(filename).download_blob().readall()
        container_client.delete_blob(filename)
        return file_data
    except Exception:
        log.error(traceback.format_exc())
