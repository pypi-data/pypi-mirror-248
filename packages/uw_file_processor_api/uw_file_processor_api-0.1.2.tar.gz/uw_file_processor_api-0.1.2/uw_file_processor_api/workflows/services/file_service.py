import io
import os

import boto3


def get_file_from_s3(bucket: str, file_key: str):
    if bucket in [None, ''] or file_key in [None, '']:
        raise Exception('Invalid arguments')

    s3_client = boto3.client('s3')

    response = s3_client.get_object(
        Bucket=bucket, Key=file_key)

    return io.BytesIO(response['Body'].read())


def download_file_from_s3(bucket: str, file_key: str, path_to_save: str = None, save_file: bool = False) -> io.BytesIO:
    if bucket in [None, ''] or file_key in [None, '']:
        raise Exception('Invalid arguments')

    s3_client = boto3.client('s3')

    response = s3_client.get_object(Bucket=bucket, Key=file_key)

    file_content = response['Body'].read()

    file_name = os.path.basename(file_key)

    if save_file:
        if path_to_save in [None, '']:
            raise Exception('path to save file is required')

        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)

        with open(f'{path_to_save}/{file_name}', 'wb') as file:
            file.write(file_content)

    return io.BytesIO(file_content)


def upload_file_to_s3(bucket: str, file_key: str, file: io.BytesIO, metadata: dict = None):
    if bucket in [None, ''] or file_key in [None, '']:
        raise Exception('Invalid arguments')

    s3_client = boto3.client('s3')

    s3_client.put_object(Bucket=bucket, Key=file_key, Body=file, Metadata=metadata)


def get_file_metadata_from_s3(bucket: str, file_key: str):
    if bucket in [None, ''] or file_key in [None, '']:
        raise Exception('Invalid arguments')

    s3_client = boto3.client('s3')

    response = s3_client.head_object(Bucket=bucket, Key=file_key)

    return response['Metadata']


def get_file_from_local(path_to_file: str) -> io.BytesIO:
    if path_to_file in [None, '']:
        raise Exception('Invalid arguments')

    with open(path_to_file, 'rb') as file:
        return io.BytesIO(file.read())
