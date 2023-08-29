from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
import uuid
import datetime

def uploadToBlob():
    # Azure Storage Account connection string
    connection_string = "DefaultEndpointsProtocol=https;AccountName=kiszstorage;AccountKey=/qQq2wTzTs8zMI0KL4WtKFiedIH86iHAuzSUe2L2RcEGRBbfpdZNXywQO33two5l6Adtd3MJE05v+AStBDpFdA==;EndpointSuffix=core.windows.net"

    # Create a BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Container name
    container_name = "blobstoragecontainer"

    # Generate a unique name for the file (e.g., using timestamp and UUID)
    unique_filename = f"{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{str(uuid.uuid4())}.csv"

    # Local file path to upload
    local_file_path = "Feedback.csv"

    # Upload the file with the unique name
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(unique_filename)

    with open(local_file_path, "rb") as data:
        blob_client.upload_blob(data)

    print(f"File '{unique_filename}' uploaded successfully.")

def uploadToBlob2():
    # Azure Storage Account connection string
    connection_string = "DefaultEndpointsProtocol=https;AccountName=kiszstorage;AccountKey=/qQq2wTzTs8zMI0KL4WtKFiedIH86iHAuzSUe2L2RcEGRBbfpdZNXywQO33two5l6Adtd3MJE05v+AStBDpFdA==;EndpointSuffix=core.windows.net"

    # Create a BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Container name
    container_name = "blobstoragecontainer2"

    # Generate a unique name for the file (e.g., using timestamp and UUID)
    unique_filename = f"{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{str(uuid.uuid4())}.csv"

    # Local file path to upload
    local_file_path = "inputAndOutput.csv"

    # Upload the file with the unique name
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(unique_filename)

    with open(local_file_path, "rb") as data:
        blob_client.upload_blob(data)

    print(f"File '{unique_filename}' uploaded successfully.")


