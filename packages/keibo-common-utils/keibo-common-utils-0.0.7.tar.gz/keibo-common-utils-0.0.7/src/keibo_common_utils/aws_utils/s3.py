import os
import boto3
from botocore.exceptions import ClientError
from keibo_common_utils.logging_utils.p_logger import P_Logger


def upload_file(file_name: str, bucket: str, logger: P_Logger, object_name: str = None) -> bool:
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file to S3
    s3_client = boto3.client("s3")

    try:
        logger.info(f"Uploading file {file_name} to S3")
        s3_client.upload_file(file_name, bucket, object_name)
        logger.info(f"{file_name} uploaded successfully to S3")
    except ClientError as e:
        logger.error(e)

        return False

    return True
