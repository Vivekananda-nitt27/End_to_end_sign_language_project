import os
from dataclasses import dataclass
from datetime import datetime
import platform
from signLanguage.constant.training_pipeline import *


# Timestamp for artifacts
TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")


@dataclass
class TrainingPipelineConfig:
    artifacts_dir: str = os.path.join(ARTIFACTS_DIR, TIMESTAMP)


# Create a single instance to reuse across configs
training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()


@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join(
        training_pipeline_config.artifacts_dir,
        DATA_INGESTION_DIR_NAME
    )

    
    feature_store_file_path: str = (
        "C:/sign_data"
        if platform.system() == "Windows"
        else os.path.join(
            data_ingestion_dir,
            DATA_INGESTION_FEATURE_STORE_DIR
        )
    )

    data_download_url: str = DATA_DOWNLOAD_URL
    
    
@dataclass
class DataValidationConfig:
    data_validation_dir: str = os.path.join(
        training_pipeline_config.artifacts_dir,
        DATA_VALIDATION_DIR_NAME
    )

    valid_status_file_dir: str = os.path.join(
        data_validation_dir,
        DATA_VALIDATION_STATUS_FILE
    )

    required_file_list = DATA_VALIDATION_ALL_REQUIRED_FILES

