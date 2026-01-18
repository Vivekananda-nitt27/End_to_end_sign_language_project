import os
import sys
import shutil

from signLanguage.logger import logging
from signLanguage.exception import SignException
from signLanguage.entity.config_entity import DataValidationConfig
from signLanguage.entity.artifacts_entity import (
    DataIngestionArtifact,
    DataValidationArtifact
)


class DataValidation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig,
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
        except Exception as e:
            raise SignException(e, sys)

    def validate_all_files_exist(self) -> bool:
        try:
            validation_status = True

            feature_store_path = self.data_ingestion_artifact.feature_store_path
            existing_files = os.listdir(feature_store_path)

            for required_file in self.data_validation_config.required_file_list:
                if required_file not in existing_files:
                    validation_status = False
                    break

            os.makedirs(
                self.data_validation_config.data_validation_dir,
                exist_ok=True
            )

            with open(
                self.data_validation_config.valid_status_file_dir, "w"
            ) as f:
                f.write(f"Validation status: {validation_status}")

            return validation_status

        except Exception as e:
            raise SignException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        logging.info(
            "Entered initiate_data_validation method of DataValidation class"
        )

        try:
            status = self.validate_all_files_exist()

            data_validation_artifact = DataValidationArtifact(
                validation_status=status
            )

            logging.info(
                "Exited initiate_data_validation method of DataValidation class"
            )
            logging.info(
                f"Data validation artifact: {data_validation_artifact}"
            )

            if status:
                shutil.copy(
                    self.data_ingestion_artifact.data_zip_file_path,
                    os.getcwd()
                )

            return data_validation_artifact

        except Exception as e:
            raise SignException(e, sys)
