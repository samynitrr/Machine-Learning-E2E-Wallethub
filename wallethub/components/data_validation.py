from wallethub.entity.config_entity import DataValidationConfig
from wallethub.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from wallethub.exception import WallethubException
from wallethub.logger import logging
from wallethub.util.util import read_yaml_file
import os,sys
import pandas as pd
import json
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab

class DataValidation:

    def __init__(self,
    data_validation_config:DataValidationConfig,
    data_ingestion_artifact: DataIngestionArtifact
    ):        
        try:
            logging.info(f"{'='*20}Data Validation log started.{'='*20}")
            self.data_validation_config= data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise WallethubException(e,sys) from e

    def get_train_and_test_df(self):
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            return train_df, test_df
        except Exception as e:
            raise WallethubException(e,sys) from e

    def train_test_file_exists(self)-> bool:
        try:
            logging.info(f"Checking if train and test file is available")
            train_file_exists = False
            test_file_exists = False

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_file_exists = os.path.exists(train_file_path)
            test_file_exists = os.path.exists(test_file_path)

            is_available = train_file_exists and test_file_exists
            if not is_available:
                training_file = self.data_ingestion_artifact.train_file_path
                testing_file = self.data_ingestion_artifact.test_file_path
                message = f"Train File : {training_file} or Testing file: {testing_file} "\
                    "is not available"
                raise Exception(message)
            logging.info(f"Train and Test file exits? -> {is_available}")
            return is_available
        except Exception as e:
            raise WallethubException(e, sys) from e    
    

    def validate_dataset_schema(self)-> bool:
        try:
            validation_status = False
            # Read Schema information
            schema_info = read_yaml_file(self.data_validation_config.schema_file_path)
            schema_columns = list(schema_info["columns"].keys())
            schema_domain_values = list(schema_info["domain_value"]["ocean_proximity"])
            schema_number_of_columns = len(schema_columns)

            # Read Train and Test file
            df_train,df_test = self.get_train_and_test_df()

            # Read Train File information
            train_columns = list(df_train.columns)
            train_no_of_columns = len(train_columns)
            train_domain_values = list(df_train["ocean_proximity"].value_counts().index)

            # Read Test file information
            test_columns = list(df_test.columns)
            test_no_of_columns = len(test_columns)
            test_domain_values = list(df_test["ocean_proximity"].value_counts().index)

            # 1. Number of Columns            
            is_number_of_columns_match = (schema_number_of_columns == train_no_of_columns)\
                                         and \
                                        (schema_number_of_columns == test_no_of_columns)
                      

            # 2. Name of Columns
            schema_columns.sort()
            train_columns.sort()
            test_columns.sort()
            if (schema_columns == train_columns) and (schema_columns == test_columns):
                is_name_of_columns_match = True
            else:
                is_name_of_columns_match = False

             # 3. Ocean_proximity values
            schema_domain_values.sort()
            train_domain_values.sort()
            test_domain_values.sort()
            if (schema_domain_values == train_domain_values) and (schema_domain_values == test_domain_values):
                is_domain_value_match = True
            else:
                is_domain_value_match = False
            if not is_domain_value_match:
                pass              


            validation_status = is_number_of_columns_match and is_name_of_columns_match and is_domain_value_match
            return validation_status
        except Exception as e:
            raise WallethubException(e,sys) from e   
    

    def save_and_get_data_drift_report(self):
        try:
            profile = Profile(sections=[DataDriftProfileSection()])
            train_df,test_df = self.get_train_and_test_df()
            profile.calculate(train_df,test_df)
            profile.json()
            report = json.loads(profile.json())

            report_file_path = self.data_validation_config.report_file_path
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir,exist_ok=True) 

            with open(self.data_validation_config.report_file_path,"w") as report_file:
                json.dump(report, report_file, indent=6)
            return report

        except Exception as e:
            raise WallethubException(e,sys) from e

    def save_data_drift_report_page(self):
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df,test_df = self.get_train_and_test_df()
            dashboard.calculate(train_df, test_df)

            report_page_file_path = self.data_validation_config.report_page_file_path
            report_page_dir = os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir,exist_ok=True) 

            dashboard.save(self.data_validation_config.report_page_file_path)
        except Exception as e:
            raise WallethubException(e,sys) from e

    def is_data_drift_found(self):
        try:
            report = self.save_and_get_data_drift_report()
            self.save_data_drift_report_page()
            is_data_drift_found = report['data_drift']['data']['metrics']['dataset_drift']
            return is_data_drift_found
        except Exception as e:
            raise WallethubException(e,sys) from e


    def initiate_data_validation(self)-> DataValidationArtifact:
        try:
            self.train_test_file_exists()
            self.validate_dataset_schema()
            self.is_data_drift_found()

            data_validation_artifact = DataValidationArtifact(
                schema_file_path=self.data_validation_config.schema_file_path,
                report_file_path= self.data_validation_config.report_file_path,
                report_page_file_path=self.data_validation_config.report_page_file_path,
                is_validated= self.validate_dataset_schema(),
                is_data_drift_found = self.is_data_drift_found(),
                message="Data Validated Successfully"

            )
            logging.info(f"Data Validation artifact:[{data_validation_artifact}]")
            return data_validation_artifact
            
        except Exception as e:
            raise WallethubException(e,sys) from e

    