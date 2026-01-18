import os

# Common artifacts directory
ARTIFACTS_DIR: str = "artifacts"

"""
Data Ingestion related constants start with DATA_INGESTION_ variable name
"""

DATA_INGESTION_DIR_NAME: str = "data_ingestion"

DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"

DATA_DOWNLOAD_URL: str = (
    "https://github.com/Vivekananda-nitt27/End_to_end_sign_language_project/raw/main/data/sign_language_data.zip"
)

"""
Data Validation related constants start with DATA_VALIDATION_ variable name
"""

DATA_VALIDATION_DIR_NAME: str = "data_validation"

DATA_VALIDATION_STATUS_FILE: str = "status.txt"

DATA_VALIDATION_ALL_REQUIRED_FILES = [
    "train",
    "test",
    "data.yaml"
]
