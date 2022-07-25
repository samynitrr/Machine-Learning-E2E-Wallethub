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
DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY = "transformed_dir"
DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DIR_KEY = "transformed_train_dir"
DATA_TRANSFORMATION_TRANSFORMED_TEST_DIR_KEY = "transformed_test_dir"
DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY = "preprocessing_dir"
DATA_TRANSFORMATION_PREPROCESSED_FILE_NAME_KEY = "preprocessed_object_file_name"
DATA_TRANSFORMATION_ARTIFACT_DIR = "data_transformation"

####### MODEL TRAINER related Variable
MODEL_TRAINER_ARTIFACT_DIR = "model_trainer"
MODEL_TRAINER_CONFIG_KEY = "model_trainer_config"
MODEL_TRAINER_TRAINED_MODEL_DIR_KEY = "trained_model_dir"
MODEL_TRAINER_TRAINED_MODEL_FILE_NAME_KEY = "model_file_name"
MODEL_TRAINER_BASE_ACCURACY_KEY = "base_accuracy"
MODEL_TRAINER_BASE_DIFF_TRAIN_TEST_ACC_KEY = "base_diff_train_test_acc"
MODEL_TRAINER_CONFIG_DIR_KEY = "model_config_dir"
MODEL_TRAINER_CONFIG_FILE_NAME_KEY = "model_config_file_name"
MODEL_TRAINER_TRAINED_MODEL_PARAMS_DIR_KEY = "trained_model_params_dir"
MODEL_TRAINER_PARAMS_FILE_NAME_KEY = "params_file_name"


####### MODEL EVALUATION related Variable
MODEL_EVALUATION_CONFIG_KEY = "model_evaluation_config"
MODEL_EVALUATION_FILE_NAME_KEY = "model_evaluation_file_name"
MODEL_EVALUATION_ARTIFACT_DIR = "model_evaluation"
  
####### MODEL PUSHER related Variable
MODEL_PUSHER_CONFIG_KEY = "model_pusher_config"
MODEL_PUSHER_MODEL_EXPORT_DIR_KEY = "model_export_dir"
MODEL_PUSHER_ARTIFACT_DIR = "model_pusher"


####### MODEL related variable
BEST_MODEL_KEY = "best_model"
HISTORY_KEY = "history"
MODEL_PATH_KEY = "model_path"

EXPERIMENT_DIR_NAME="experiment"
EXPERIMENT_FILE_NAME="experiment.csv"
