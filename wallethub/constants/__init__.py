import os


#------------------- CONFIG YAML FILE related variables ---------------------#
ROOT_DIR = os.getcwd()

CONFIG_DIR = 'config'

CONFIG_FILE_NAME = 'config.yaml'
MODEL_FILE_NAME = 'model.yaml'
SCHEMA_FILE_NAME = 'schema.yaml'

CONFIG_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME)
MODEL_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_DIR,MODEL_FILE_NAME)
SCHEMA_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_DIR,SCHEMA_FILE_NAME)

########### SCHEMA KEYS

DATA_SCHEMA_COLUMN_KEY = "columns"
DATA_SCHEMA_DOMAIN_VALUE_KEY = "domain_value"
DATA_SCHEMA_NUMERICAL_COLUMN_KEY = "numerical_columns"
DATA_SCHEMA_CATEGORICAL_COLUMN_KEY = "categorical_columns"
DATA_SCHEMA_TARGET_COLUMN_KEY = "target_column"

####### TRAINING PIPELINE related Variable

TRAINING_PIPELINE_CONFIG_KEY = "training_pipeline_config"
TRAINING_PIPELINE_ARTIFACT_DIR_KEY = "artifact_dir"
TRAINING_PIPELINE_NAME_KEY = "pipeline_name"


####### DATA INGESTION related Variable

DATA_INGESTION_CONFIG_KEY = "data_ingestion_config"
DATA_INGESTION_ARTIFACT_DIR = "data_ingestion"
DATA_INGESTION_DOWNLOAD_URL_KEY = "dataset_download_url"
DATA_INGESTION_DATASET_FILE_NAME_KEY = "dataset_file_name"
DATA_INGESTION_RAW_DATA_DIR_KEY = "raw_data_dir"
DATA_INGESTION_ZIP_DOWNLOAD_DIR_KEY = "zip_download_dir"
DATA_INGESTION_INGESTED_DIR_NAME_KEY = "ingested_dir"
DATA_INGESTION_TRAIN_DIR_KEY = "ingested_train_dir"
DATA_INGESTION_TEST_DIR_KEY = "ingested_test_dir"