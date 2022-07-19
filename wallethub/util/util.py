import yaml
import os
import sys
import dill
from datetime import datetime
import pandas as pd
import numpy as np
from wallethub.exception import WallethubException
from wallethub.constants import *
import requests

def log_file_name():
        return f"log_{get_current_time_stamp()}.log"


def write_yaml_file(file_path:str,data:dict=None):
    """
    Create yaml file 
    file_path: str
    data: dict
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path,"w") as yaml_file:
            if data is not None:
                yaml.dump(data,yaml_file)
    except Exception as e:
        raise WallethubException(e,sys)

def read_yaml_file(file_path:str)->dict:
    """
    This function takes the yaml file path as an input,
    reads the yaml file safely and returns the content
    of the yaml file.
    --------------------------------------------------
    return: dict    
    """     
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file) 
    except Exception as e:
        raise WallethubException(e,sys) from e


def get_current_time_stamp():
    """
    This function return the current timestamp in the defined format
    ----------------------------------------------------------------
    return: %Y-%m-%d-%H-%M-%S
    """
    return f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"


def get_log_dataframe(file_path):
    data=[]
    with open(file_path) as log_file:
        for line in log_file.readlines():
            data.append(line.split("^;"))

    log_df = pd.DataFrame(data)
    columns=["Time stamp","Log Level","line number","file name","function name","message"]
    log_df.columns=columns
    
    log_df["log_message"] = log_df['Time stamp'].astype(str) +":$"+ log_df["message"]

    return log_df[["log_message"]]


def generate_and_save_schema_file(data_file_path:str,
                                 target_column_name:str
                                 )->str:
        """
        Reads a data file and returns the schema as a dictionary.
        file_path: str
        """
        try:
            df = pd.read_csv(data_file_path)
            columns = df.columns
            data_types = list(map(lambda x:str(x).replace("dtype('","").replace("')",""), df.dtypes.values))
            columns_values = dict(zip(columns,data_types))
            num_columns = []
            cat_columns=[]
            domain_value = {}
            for column in columns_values:
                if columns_values[column] == 'object':
                    domain_value[column]= list(df[column].value_counts().index)
                    cat_columns.append(column)
                else:
                    num_columns.append(column)
            if target_column_name in columns_values:
                if target_column_name in num_columns:
                    num_columns.remove(target_column_name)
                else:
                    cat_columns.remove(target_column_name) 
            else:
                raise Exception(f"Target Column Name: [{target_column_name}] not in dataset."\
                     "Please ensure the spelling of the target column name is correct")
            
            schema = {
                "columns":
                    columns_values,
                
                "numerical_columns":
                    num_columns,

                "categorical_columns":
                    cat_columns,
                
                "target_column": 
                    target_column_name,

                "domain_value":
                    domain_value
                     }
            schema_dir = "schema"
            os.makedirs(schema_dir, exist_ok=True)
            schema_file_name = "schema.yaml"
            save_schema_file_path = os.path.join(
                ROOT_DIR,
                schema_dir,
                schema_file_name
                )
            with open(save_schema_file_path, "w") as schema_file:
                yaml.dump(schema, schema_file)
            return save_schema_file_path 
        except Exception as e:
            raise WallethubException(e,sys) from e


def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise WallethubException(e, sys) from e


def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise WallethubException(e, sys) from e


def save_object(file_path:str,obj):
    """
    file_path: str
    obj: Any sort of object
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise WallethubException(e,sys) from e


def load_object(file_path:str):
    """
    file_path: str
    """
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise WallethubException(e,sys) from e

def load_dataset(file_path:str, schema_file_path:str)->pd.DataFrame:
    try:
        dataset_schema = read_yaml_file(schema_file_path)
        schema = dataset_schema[DATA_SCHEMA_COLUMN_KEY]
        dataframe = pd.read_csv(file_path)
        error_message = ""

        for column in dataframe.columns:
            if column in schema.keys():
                dataframe[column].astype(schema[column])
            else:
                error_message = f"{error_message} \nColumn: [{column}] is not in the schema"

        if len(error_message)>0:
            raise Exception(error_message)
        return dataframe
    except Exception as e:
        raise WallethubException(e,sys) from e



##Download the file from Google drive
def get_gdrive_file_id(url):
    file_url = url
    file_id= file_url[file_url.find('d/')+2: file_url.find('/view') ]
    return file_id

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)




    



