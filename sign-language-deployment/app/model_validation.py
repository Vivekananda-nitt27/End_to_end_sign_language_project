import os
import sys
from app.exception import SignException
from app.logger import logger as logging


class ModelValidation:
    def __init__(self, model_path: str):
        self.model_path = model_path

    def validate(self) -> bool:
        logging.info("Starting model artifact validation")
        try:
            if not os.path.exists(self.model_path):
                logging.error("Model file not found")
                return False

            if os.path.getsize(self.model_path) == 0:
                logging.error("Model file is empty")
                return False

            logging.info("Model artifact validation successful")
            return True

        except Exception as e:
            raise SignException(e, sys) from e
