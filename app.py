from flask import Flask, request
import sys
from wallethub.util.util import read_yaml_file, write_yaml_file
from wallethub.logger import logging
from wallethub.exception import WallethubException
import os, sys
import json
from wallethub.get_config.configuration import Configuration
from wallethub.constants import CONFIG_DIR, EXPERIMENT_FILE_NAME, MODEL_FILE_PATH
from wallethub.util.util import get_current_time_stamp, get_log_dataframe, custom_describe
from wallethub.pipeline.pipeline import Pipeline
from wallethub.entity.wallethub_predictor import Predictor, Data
from flask import send_file, abort, render_template
import plotly
import plotly.express as px
import pandas as pd
ROOT_DIR = os.getcwd()
LOG_FOLDER_NAME = "PRODUCTION_LOGS"
PIPELINE_FOLDER_NAME = "wallethub"
SAVED_MODELS_DIR_NAME = "model_registry"
MODEL_CONFIG_FILE_PATH = MODEL_FILE_PATH
LOG_DIR = os.path.join(ROOT_DIR, LOG_FOLDER_NAME)
PIPELINE_DIR = os.path.join(ROOT_DIR, PIPELINE_FOLDER_NAME)
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)
RAW_FILE_PATH = os.path.join(PIPELINE_DIR,"artifact", "data_ingestion", "2022-07-25-17-25-42" ,"raw_data","dataset_00_with_header.csv" )
EXPERIMENT_FILE_PATH = os.path.join(PIPELINE_DIR,"artifact", "experiment","experiment.csv")

DATA_KEY = "data"
VALUE_KEY = "y"

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return str(e)

@app.route('/projects', methods=['GET', 'POST'])
def project():
    try:
        return render_template('project.html')
    except Exception as e:
        return str(e)

@app.route('/test', methods=['GET', 'POST'])
def test():
    try:
        df = pd.read_csv(RAW_FILE_PATH) 
        describe_df = custom_describe(df)
        context = {
            "describe": describe_df.to_html(classes='table table-striped col-12')
        }
        return render_template('test.html', context=context)
    except Exception as e:
        return str(e)

@app.route('/data', methods=['GET', 'POST'])
def data():
    try:
        # Graph One
        df = pd.read_csv(RAW_FILE_PATH) 
        # describe_df = custom_describe(df)
        # context = {
        #     "describe": describe_df.to_html(classes='table table-striped col-12')
        # }
        fig1 = px.histogram(df.x001, x="x001", hover_data=['x001'])        
        graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
        fig2 = px.box(df.x001,x="x001")        
        graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('data.html', title = "Datasets", graph1JSON = graph1JSON, graph2JSON = graph2JSON )
    except Exception as e:
        return str(e)

@app.route('/model', methods=['GET', 'POST'])
def model():
    try:
        if request.method == 'POST':
            model_config = request.form['new_model_config']
            model_config = model_config.replace("'", '"')
            print(model_config)
            model_config = json.loads(model_config)

            write_yaml_file(file_path=MODEL_CONFIG_FILE_PATH, data=model_config)

        model_config = read_yaml_file(file_path=MODEL_CONFIG_FILE_PATH)
        model_train = False
        # message = ""
        # context= {"message": message}
        # if model_train:
            
        #     pipeline = Pipeline(config=Configuration(current_time_stamp=get_current_time_stamp()))
        #     if not Pipeline.experiment.running_status:
        #         message = "Training started."
        #         pipeline.start()
        #     else:
        #         message = "Training is already in progress."
        #     context = {
        #         "message": message
        #     }
        if os.path.exists(EXPERIMENT_FILE_PATH):
            df= pd.read_csv(EXPERIMENT_FILE_PATH)
            limit=-5
            experiment_df =  df[limit:].drop(columns=["experiment_file_path","initialization_timestamp"],axis=1)
        else:
            experiment_df = pd.DataFrame()
         
        context2 = {
            "experiment": experiment_df.to_html(classes='table table-striped col-12')
        }
        return render_template('model.html',result={"model_config": model_config}, context2=context2)
    except Exception as e:
        return str(e)


@app.route('/artifact', defaults={'req_path': 'wallethub'})
@app.route('/artifact/<path:req_path>')
def render_artifact_dir(req_path):
    os.makedirs("wallethub", exist_ok=True)
    # Joining the base and the requested path
    print(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        if ".html" in abs_path:
            with open(abs_path, "r", encoding="utf-8") as file:
                content = ''
                for line in file.readlines():
                    content = f"{content}{line}"
                return content
        return send_file(abs_path)

    # Show directory contents
    files = {os.path.join(abs_path, file_name): file_name for file_name in os.listdir(abs_path) if
             "artifact" in os.path.join(abs_path, file_name)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('artifacts.html', result=result)








# @app.route('/train', methods=['GET', 'POST'])
# def train():
#     message = ""
#     pipeline = Pipeline(config=Configuration(current_time_stamp=get_current_time_stamp()))
#     if not Pipeline.experiment.running_status:
#         message = "Training started."
#         pipeline.start()
#     else:
#         message = "Training is already in progress."
#     context = {
#         "experiment": pipeline.get_experiments_status().to_html(classes='table table-striped col-12'),
#         "message": message
#     }
#     return render_template('train.html', context=context)


# @app.route('/predict', methods=['GET', 'POST'])
# def predict():
#     context = {
#         DATA_KEY: None,
#         VALUE_KEY: None
#     }

#     if request.method == 'POST':
#         longitude = float(request.form['longitude'])
#         latitude = float(request.form['latitude'])
#         housing_median_age = float(request.form['housing_median_age'])
#         total_rooms = float(request.form['total_rooms'])
#         total_bedrooms = float(request.form['total_bedrooms'])
#         population = float(request.form['population'])
#         households = float(request.form['households'])
#         median_income = float(request.form['median_income'])
#         ocean_proximity = request.form['ocean_proximity']

#         housing_data = HousingData(longitude=longitude,
#                                    latitude=latitude,
#                                    housing_median_age=housing_median_age,
#                                    total_rooms=total_rooms,
#                                    total_bedrooms=total_bedrooms,
#                                    population=population,
#                                    households=households,
#                                    median_income=median_income,
#                                    ocean_proximity=ocean_proximity,
#                                    )
#         housing_df = housing_data.get_housing_input_data_frame()
#         housing_predictor = HousingPredictor(model_dir=MODEL_DIR)
#         median_housing_value = housing_predictor.predict(X=housing_df)
#         context = {
#             HOUSING_DATA_KEY: housing_data.get_housing_data_as_dict(),
#             MEDIAN_HOUSING_VALUE_KEY: median_housing_value,
#         }
#         return render_template('predict.html', context=context)
#     return render_template("predict.html", context=context)


# @app.route('/saved_models', defaults={'req_path': 'saved_models'})
# @app.route('/saved_models/<path:req_path>')
# def saved_models_dir(req_path):
#     os.makedirs("saved_models", exist_ok=True)
#     # Joining the base and the requested path
#     print(f"req_path: {req_path}")
#     abs_path = os.path.join(req_path)
#     print(abs_path)
#     # Return 404 if path doesn't exist
#     if not os.path.exists(abs_path):
#         return abort(404)

#     # Check if path is a file and serve
#     if os.path.isfile(abs_path):
#         return send_file(abs_path)

#     # Show directory contents
#     files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

#     result = {
#         "files": files,
#         "parent_folder": os.path.dirname(abs_path),
#         "parent_label": abs_path
#     }
#     return render_template('saved_models_files.html', result=result)





# @app.route(f'/logs', defaults={'req_path': f'{LOG_FOLDER_NAME}'})
# @app.route(f'/{LOG_FOLDER_NAME}/<path:req_path>')
# def render_log_dir(req_path):
#     os.makedirs(LOG_FOLDER_NAME, exist_ok=True)
#     # Joining the base and the requested path
#     logging.info(f"req_path: {req_path}")
#     abs_path = os.path.join(req_path)
#     print(abs_path)
#     # Return 404 if path doesn't exist
#     if not os.path.exists(abs_path):
#         return abort(404)

#     # Check if path is a file and serve
#     if os.path.isfile(abs_path):
#         log_df = get_log_dataframe(abs_path)
#         context = {"log": log_df.to_html(classes="table-striped", index=False)}
#         return render_template('log.html', context=context)

#     # Show directory contents
#     files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

#     result = {
#         "files": files,
#         "parent_folder": os.path.dirname(abs_path),
#         "parent_label": abs_path
#     }
#     return render_template('log_files.html', result=result)


if __name__ == "__main__":
    app.run()