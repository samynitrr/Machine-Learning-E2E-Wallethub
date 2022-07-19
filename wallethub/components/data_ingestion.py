from wallethub.entity.config_entity import DataIngestionConfig
from wallethub.entity.artifact_entity import DataIngestionArtifact
from wallethub.exception import WallethubException
from wallethub.logger import logging
from wallethub.util.util import get_gdrive_file_id, download_file_from_google_drive
import os,sys
import tarfile
import zipfile
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
import numpy as np
class DataIngestion:

    def __init__(self,
    data_ingestion_config:DataIngestionConfig):        
        try:
            logging.info(f"{'='*20}Data Ingestion log started.{'='*20}")
            self.data_ingestion_config= data_ingestion_config
            pass
        except Exception as e:
            raise WallethubException(e,sys) from e

    def download_data(self) -> str:
        try:
            #extract remote url to download dataset
            download_url = self.data_ingestion_config.dataset_download_url 
            data_file_name = self.data_ingestion_config.dataset_file_name 

            # folder location to download file
            zip_download_dir = self.data_ingestion_config.zip_download_dir

            if os.path.exists(zip_download_dir):
                os.remove(zip_download_dir)

            os.makedirs(zip_download_dir, exist_ok=True)       
            

            zip_file_path = os.path.join(zip_download_dir,data_file_name)

            logging.info(f"Downloading file from :[{download_url}] into : [{zip_file_path}]")

            #download the file to desired location
            file_id = get_gdrive_file_id(download_url)
            download_file_from_google_drive(file_id, zip_file_path)

            logging.info(f"File: [{zip_file_path}] has been downloaded successfully")

            return zip_file_path


        except Exception as e:
            raise WallethubException(e,sys) from e

    def extract_zip_file(self, zip_file_path:str):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir, exist_ok=True)
            logging.info(f"Extracting zip file: [{zip_file_path}] into: [{raw_data_dir}]")
            
            # Using tarfile to extract all the contents of the .zip file
            # zip_file path is the location of the .zip file and
            # raw_data_dir is the location of the extracted file
            
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(raw_data_dir)

            logging.info(f"Extracting completed successfully")

        except Exception as e:
            raise WallethubException(e,sys) from e

    def split_data_as_train_test(self):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            file_name = os.listdir(raw_data_dir)[0]

            file_path = os.path.join(raw_data_dir, file_name)

            logging.info(f"Reading csv file: [{file_path}]")
            df = pd.read_csv(file_path)

            df["temp_y"] = pd.cut(
                df["y"],
                bins = [300, 400, 500, 600, 700, 800, np.inf],
                labels=[1,2,3,4,5,6]
            )

            logging.info(f"Splitting data into train and test")
            strat_train_set = None
            strat_test_set = None

            split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

            for train_index, test_index in split.split(df, df["temp_y"]):
                strat_train_set = df.loc[train_index].drop(["temp_y"], axis=1)
                strat_test_set = df.loc[test_index].drop(["temp_y"], axis=1)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir, file_name)
            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir, file_name)

            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True) 
                logging.info(f"Exporting training dataset to file: [{train_file_path}]")
                strat_train_set.to_csv(train_file_path,index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir,exist_ok=True)
                logging.info(f"Exporting test dataset to file: [{test_file_path}]")    
                strat_test_set.to_csv(test_file_path,index=False)       

            data_ingestion_artifact = DataIngestionArtifact(train_file_path = train_file_path,
            test_file_path = test_file_path,
            is_ingested = True,
            message=f"Data ingestion completed successfully"
            )
            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact

        except Exception as e:
            raise WallethubException(e,sys) from e

    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            zip_file_path = self.download_data()
            self.extract_zip_file(zip_file_path=zip_file_path)
            return self.split_data_as_train_test()
        except Exception as e:
            raise WallethubException(e,sys) from e

