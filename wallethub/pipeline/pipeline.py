from wallethub.get_config.configuration import Configuration
from wallethub.logger import logging
from wallethub.exception import WallethubException
from wallethub.entity.artifact_entity import *
from wallethub.entity.config_entity import *
from wallethub.components.data_ingestion import DataIngestion
from wallethub.components.data_validation import DataValidation
import os, sys
import pandas  as pd


class Pipeline():

    def __init__(self, config: Configuration) -> None:
        try:
            self.config = config
        except Exception as e:
            raise WallethubException(e, sys) from e

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise WallethubException(e, sys) from e

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) \
            -> DataValidationArtifact:
        try:
            data_validation = DataValidation(data_validation_config=self.config.get_data_validation_config(),
                                             data_ingestion_artifact=data_ingestion_artifact
                                             )
            return data_validation.initiate_data_validation()
        except Exception as e:
            raise WallethubException(e, sys) from e   

    
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            
            logging.info(f"Pipeline run successfully completed")
        except Exception as e:
            raise WallethubException(e, sys) from e


