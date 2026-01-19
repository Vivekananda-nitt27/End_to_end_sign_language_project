import sys
import os
import boto3
import pickle
from io import StringIO, BytesIO
from typing import Union, List
from pandas import DataFrame
from mypy_boto3_s3.service_resource import Bucket

from signLanguage.exception import SignException
from signLanguage.logger import logging


class S3Operation:
    def __init__(self):
        try:
            self.s3_client = boto3.client("s3")
            self.s3_resource = boto3.resource("s3")
        except Exception as e:
            raise SignException(e, sys) from e

    # -------------------------------------------------------------------------
    # READ OBJECT
    # -------------------------------------------------------------------------
    @staticmethod
    def read_object(
        object_name,
        decode: bool = True,
        make_readable: bool = False
    ) -> Union[StringIO, str, bytes]:
        """
        Reads an S3 object body
        """
        logging.info("Entered the read_object method of S3Operation class")
        try:
            data = (
                object_name.get()["Body"].read().decode()
                if decode
                else object_name.get()["Body"].read()
            )
            return StringIO(data) if make_readable else data

        except Exception as e:
            raise SignException(e, sys) from e

    # -------------------------------------------------------------------------
    # GET BUCKET
    # -------------------------------------------------------------------------
    def get_bucket(self, bucket_name: str) -> Bucket:
        """
        Returns S3 bucket resource
        """
        logging.info("Entered the get_bucket method of S3Operation class")
        try:
            return self.s3_resource.Bucket(bucket_name)
        except Exception as e:
            raise SignException(e, sys) from e

    # -------------------------------------------------------------------------
    # CHECK IF MODEL EXISTS
    # -------------------------------------------------------------------------
    def is_model_present(self, bucket_name: str, s3_model_key: str) -> bool:
        """
        Checks whether model exists in S3 bucket
        """
        logging.info("Entered the is_model_present method of S3Operation class")
        try:
            bucket = self.get_bucket(bucket_name)
            objs = list(bucket.objects.filter(Prefix=s3_model_key))
            return len(objs) > 0

        except Exception as e:
            raise SignException(e, sys) from e

    # -------------------------------------------------------------------------
    # GET FILE OBJECT
    # -------------------------------------------------------------------------
    def get_file_object(
        self,
        filename: str,
        bucket_name: str
    ) -> Union[List[object], object]:
        """
        Gets file object(s) from S3 bucket
        """
        logging.info("Entered the get_file_object method of S3Operation class")
        try:
            bucket = self.get_bucket(bucket_name)
            objs = [obj for obj in bucket.objects.filter(Prefix=filename)]
            return objs[0] if len(objs) == 1 else objs

        except Exception as e:
            raise SignException(e, sys) from e

    # -------------------------------------------------------------------------
    # CREATE FOLDER (PREFIX)
    # -------------------------------------------------------------------------
    def create_folder(self, bucket_name: str, folder_name: str) -> None:
        """
        Creates folder (prefix) in S3
        """
        logging.info("Entered the create_folder method of S3Operation class")
        try:
            if not folder_name.endswith("/"):
                folder_name += "/"

            self.s3_client.put_object(Bucket=bucket_name, Key=folder_name)
            logging.info(f"Folder {folder_name} created in bucket {bucket_name}")

        except Exception as e:
            raise SignException(e, sys) from e

    # -------------------------------------------------------------------------
    # UPLOAD FILE
    # -------------------------------------------------------------------------
    def upload_file(
        self,
        file_path: str,
        bucket_name: str,
        s3_key: str
    ) -> None:
        """
        Uploads local file to S3
        """
        logging.info("Entered the upload_file method of S3Operation class")
        try:
            self.s3_client.upload_file(
                Filename=file_path,
                Bucket=bucket_name,
                Key=s3_key
            )
            logging.info(f"Uploaded {file_path} to s3://{bucket_name}/{s3_key}")

        except Exception as e:
            raise SignException(e, sys) from e

    # -------------------------------------------------------------------------
    # UPLOAD DATAFRAME AS CSV
    # -------------------------------------------------------------------------
    def upload_df_as_csv(
        self,
        df: DataFrame,
        bucket_name: str,
        s3_key: str,
        index: bool = False
    ) -> None:
        """
        Uploads Pandas DataFrame as CSV to S3
        """
        logging.info("Entered the upload_df_as_csv method of S3Operation class")
        try:
            buffer = StringIO()
            df.to_csv(buffer, index=index)

            self.s3_client.put_object(
                Bucket=bucket_name,
                Key=s3_key,
                Body=buffer.getvalue()
            )

            logging.info(f"DataFrame uploaded to s3://{bucket_name}/{s3_key}")

        except Exception as e:
            raise SignException(e, sys) from e

    # -------------------------------------------------------------------------
    # LOAD MODEL FROM S3
    # -------------------------------------------------------------------------
    def load_model_from_s3(
        self,
        bucket_name: str,
        s3_model_key: str
    ):
        """
        Loads pickle / torch model from S3
        """
        logging.info("Entered the load_model_from_s3 method of S3Operation class")
        try:
            response = self.s3_client.get_object(
                Bucket=bucket_name,
                Key=s3_model_key
            )

            model_bytes = response["Body"].read()
            model = pickle.loads(model_bytes)

            logging.info("Model loaded successfully from S3")
            return model

        except Exception as e:
            raise SignException(e, sys) from e

    # -------------------------------------------------------------------------
    # DOWNLOAD FILE FROM S3
    # -------------------------------------------------------------------------
    def download_file(
        self,
        bucket_name: str,
        s3_key: str,
        download_path: str
    ) -> None:
        """
        Downloads file from S3 to local system
        """
        logging.info("Entered the download_file method of S3Operation class")
        try:
            self.s3_client.download_file(
                Bucket=bucket_name,
                Key=s3_key,
                Filename=download_path
            )

            logging.info(f"Downloaded s3://{bucket_name}/{s3_key} to {download_path}")

        except Exception as e:
            raise SignException(e, sys) from e
