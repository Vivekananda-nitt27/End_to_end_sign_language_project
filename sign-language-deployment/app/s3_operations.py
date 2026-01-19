import sys
import boto3
from app.exception import SignException
from app.logger import logger as logging



class S3Operation:
    def __init__(self):
        self.s3_client = boto3.client("s3")
    
    def read_object(self, bucket_name: str, object_name: str, decode: bool = True):
     try:
        obj = self.s3_client.get_object(Bucket=bucket_name, Key=object_name)
        data = obj["Body"].read()
        return data.decode() if decode else data
     except Exception as e:
        raise SignException(e, sys) from e


    def upload_file(self, file_path: str, bucket_name: str, s3_key: str):
        try:
            logging.info(f"Uploading {file_path} to s3://{bucket_name}/{s3_key}")

            self.s3_client.upload_file(
                Filename=file_path,
                Bucket=bucket_name,
                Key=s3_key
            )

            logging.info("Upload successful")

        except Exception as e:
            logging.error(f"S3 upload failed: {e}")
            raise SignException(e, sys) from e

    def download_file(self, bucket_name: str, s3_key: str, local_path: str):
        try:
            logging.info(f"Downloading s3://{bucket_name}/{s3_key} to {local_path}")

            self.s3_client.download_file(
                Bucket=bucket_name,
                Key=s3_key,
                Filename=local_path
            )

            logging.info("Download successful")

        except Exception as e:
            logging.error(f"S3 download failed: {e}")
            raise SignException(e, sys) from e
