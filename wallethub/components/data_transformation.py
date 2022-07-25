from wallethub.entity.config_entity import DataTransformationConfig
from wallethub.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact, DataValidationArtifact
from wallethub.constants import  SCHEMA_FILE_PATH, DATA_SCHEMA_NUMERICAL_COLUMN_KEY, DATA_SCHEMA_TARGET_COLUMN_KEY
from wallethub.util.util import * 
from wallethub.exception import WallethubException
from wallethub.logger import logging
import os,sys
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer

class DataTransformation:

    def __init__(self,
    data_transformation_config:DataTransformationConfig,
    data_ingestion_artifact: DataIngestionArtifact,
    data_validation_artifact:DataValidationArtifact,
    ):        
        try:
            logging.info(f"{'='*20}Data Transformation log started.{'='*20}")
            self.data_transformation_config= data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact

            pass
        except Exception as e:
            raise WallethubException(e,sys) from e
    
    def get_data_transformer_object(self)-> ColumnTransformer:
        try:
            schema_file_path = SCHEMA_FILE_PATH
            dataset_schema = read_yaml_file(file_path=schema_file_path)
            numerical_columns =  dataset_schema[DATA_SCHEMA_NUMERICAL_COLUMN_KEY]
            
            num_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer()),
                ('standard_scaler', StandardScaler())
            ])

            
            logging.info(f"Numerical Columns: {numerical_columns}")
            preprocessing = ColumnTransformer([
                ('numerical_pipeline',num_pipeline, numerical_columns)
            ])

            return preprocessing
            
        except Exception as e:
            raise WallethubException(e,sys) from e

    def initiate_data_transformation(self)-> DataTransformationArtifact:
        try:
            logging.info(f"Obtaining preprocessing object.")
            preprocessing_obj = self.get_data_transformer_object()

            logging.info(f"Obtaining training and test file path.")
            train_file_path =  self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            schema_file_path = self.data_validation_artifact.schema_file_path
            logging.info(f"Loading training and test data as pandas dataframe.")
            train_df = load_dataset(file_path = train_file_path,schema_file_path=schema_file_path)
            test_df = load_dataset(file_path=test_file_path,schema_file_path=schema_file_path)

            schema = read_yaml_file(file_path=schema_file_path)

            target_column_name = schema[DATA_SCHEMA_TARGET_COLUMN_KEY]

            logging.info(f"Splitting input and target feature from training and testing dataframe.")
            input_feature_train_df = train_df.drop(columns=[target_column_name],axis =1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name],axis =1)
            target_feature_test_df = test_df[target_column_name]

            logging.info(f"Applying preprocessing object on training dataframe and testing dataframe")
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            transformed_train_dir = self.data_transformation_config.transformed_train_dir
            transformed_test_dir = self.data_transformation_config.transformed_test_dir

            train_file_name = os.path.basename(train_file_path).replace(".csv", ".npz")
            test_file_name = os.path.basename(test_file_path).replace(".csv", ".npz")

            transformed_train_file_path = os.path.join(transformed_train_dir, train_file_name)
            transformed_test_file_path = os.path.join(transformed_test_dir,test_file_name)

            logging.info(f"Saving transformed training and testing array.")
            save_numpy_array_data(file_path = transformed_train_file_path,array= train_arr)
            save_numpy_array_data(file_path = transformed_test_file_path,array= test_arr)

            preprocessed_object_file_path = self.data_transformation_config.preprocessed_object_file_path

            logging.info(f"Saving preprocessing object.")
            save_object(file_path=preprocessed_object_file_path, obj=preprocessing_obj)

            data_transformation_artifact = DataTransformationArtifact(
                is_transformed=True,
                message = "Data Transformed successfully",
                transformed_train_file_path= transformed_train_file_path,
                transformed_test_file_path= transformed_test_file_path,
                preprocessed_object_file_path= preprocessed_object_file_path

            )
            logging.info(f"Data Transformation artifact:[{data_transformation_artifact}]")
            return data_transformation_artifact

        except Exception as e:
            raise WallethubException(e,sys) from e