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
import shutil
from scipy.stats import skew

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
            schema_dir = "config"
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

def copyfile(source_file_path:str, dest_file_path:str):
    """
    source_file_path: str
    dest_file_path: str
    """
    try:
        dest_dir_path = os.path.dirname(dest_file_path)
        os.makedirs(dest_dir_path, exist_ok=True)
        shutil.copy(src=source_file_path, dst=dest_file_path)
        return dest_file_path
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




def custom_describe(df:pd.DataFrame)-> pd.DataFrame:
    try:
        column_name = []
        count = []
        typ = []
        missing = []
        unique = []
        mean = []
        std = []
        minm = []
        q1 = []
        median = []
        q3 = []
        maxm = []
        iqr = []
        skewness = []
        skewness_comment = []
        outlier = []
        mode = []
        for name in df.columns:
            column_name.append(name)
            count.append(df[name].count())
            
            if df[name].dtypes == int:
                typ.append('Integer')
            elif df[name].dtypes == float:
                typ.append('Float')
            else:
                typ.append('String')

            missing.append(df[name].isna().sum())
            unique.append(len(df[name].unique()))
            if df[name].dtypes != object :
                skew_score = round(skew(df[name],axis=0, bias=False ),2)
                skewness.append(skew_score)

                """
                If the skewness is between -0.5 & 0.5, the data are nearly symmetrical.

                If the skewness is between -1 & -0.5 (negative skewed) or between 0.5 & 1(positive skewed), the data are slightly skewed.

                If the skewness is lower than -1 (negative skewed) or greater than 1 (positive skewed), the data are extremely skewed.
                """
                
                if skew_score == 0:
                    skewness_comment.append("Symmetrical")
                elif skew_score > -0.5 and skew_score < 0:
                    skewness_comment.append("Fairly Symmetrical (Left)")
                elif skew_score > 0 and skew_score < 0.5:
                    skewness_comment.append("Fairly Symmetrical (Right)")
                elif skew_score > -1 and skew_score < -0.5:
                    skewness_comment.append("Moderate Left Skewed")
                elif skew_score > 0.5 and skew_score < 1:
                    skewness_comment.append("Moderate Right Skewed")
                elif skew_score < -1 :
                    skewness_comment.append("Extreme Left Skewed")
                else:
                    skewness_comment.append("Extreme Right Skewed")

                
                mean.append(df[name].mean())
                std.append(df[name].std())
                minm.append(min(df[name]))
                median.append(df[name].median())
                maxm.append(max(df[name]))
                Q1 = df[name].quantile(0.25)
                q1.append(Q1)
                Q3 = df[name].quantile(0.75) 
                q3.append(Q3)      
                
                IQR = Q3- Q1
                iqr.append(IQR)
                upperbound =  (df[name].quantile(0.75)) + (1.5*IQR)
                lowerbound =  (df[name].quantile(0.25)) - (1.5*IQR)
                
                if min(df[name]) < lowerbound or max(df[name]) > upperbound:
                    outlier.append("HasOutliers")
                else:
                    outlier.append("NoOutliers")
                mode.append("N/A")
            else:
                mode.append(df[name].mode())
                skewness.append("N/A")
                skewness_comment.append("N/A")
                mean.append("N/A")
                std.append("N/A")
                minm.append("N/A")
                median.append("N/A")
                maxm.append("N/A")
                q1.append("N/A")
                q3.append("N/A")  
                iqr.append("N/A")
                outlier.append("N/A")


        data = list(zip(column_name, typ, count,missing, unique,  mean, std, mode, minm, q1, median, q3, maxm, iqr, skewness, skewness_comment, outlier))
        column_names = ["Column Name", "Data Type", "Count", "Missing Values", "Unique Values", "Mean", "Standard Deviation" , "Mode", "Minimum", "Q1","Median","Q3","Maximum","IQR", "Skewness Score", "Skewness Comment", "Outliers"]
        describe_df = pd.DataFrame(data, columns=column_names)
            
        return describe_df
    except Exception as e:
        raise WallethubException(e, sys) from e
    



