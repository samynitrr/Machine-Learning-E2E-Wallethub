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

####### DATA VALIDATION related Variable

DATA_VALIDATION_CONFIG_KEY = "data_validation_config"
DATA_VALIDATION_SCHEMA_DIR_KEY = "schema_dir"
DATA_VALIDATION_SCHEMA_FILE_NAME_KEY = "schema_file_name"
DATA_VALIDATION_ARTIFACT_DIR = "data_validation"
DATA_VALIDATION_REPORT_FILE_NAME_KEY = "report_file_name"
DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY = "report_page_file_name"

####### DATA TRANSFORMATION related Variable

DATA_TRANSFORMATION_CONFIG_KEY = "data_transformation_config"
DATA_TRANSFORMATION_ADD_COLUMN_KEY = "add_bedroom_per_room"
DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY = "transformed_dir"
DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DIR_KEY = "transformed_train_dir"
DATA_TRANSFORMATION_TRANSFORMED_TEST_DIR_KEY = "transformed_test_dir"
DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY = "preprocessing_dir"
DATA_TRANSFORMATION_PREPROCESSED_FILE_NAME_KEY = "preprocessed_object_file_name"
DATA_TRANSFORMATION_ARTIFACT_DIR = "data_transformation"