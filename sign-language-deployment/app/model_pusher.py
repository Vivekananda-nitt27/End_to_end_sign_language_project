import sys
from app.exception import SignException
from app.logger import logger as logging
from app.s3_operations import S3Operation
from app.constant import MODEL_PUSHER_BUCKET_NAME, MODEL_PUSHER_S3_MODEL_KEY

class ModelPusher:
    def __init__(self, local_model_path: str):
        self.local_model_path = local_model_path
        self.s3_ops = S3Operation()

    def push(self):
        logging.info("Starting model push to S3")
        try:
            self.s3_ops.upload_file(
                file_path=self.local_model_path,
                bucket_name=MODEL_PUSHER_BUCKET_NAME,
                s3_key=MODEL_PUSHER_S3_MODEL_KEY
            )
            logging.info("Model pushed to S3 successfully")
        except Exception as e:
            raise SignException(e, sys) from e
