import os
import pandas as pd
import dill
import time
import datetime
from sklearn.metrics import r2_score, mean_squared_error , mean_absolute_error, mean_absolute_percentage_error



def prediction():
    start = 0
    end = 0
    start = time.time()
    print(f"{'*'*10}Prediction Started{'*'*10}")

    MODEL_DIR = os.environ["MODEL_DIR"]
    model_subdir_list= os.listdir(MODEL_DIR)
    model_subdir_list.sort()
    BEST_MODEL_DIR = model_subdir_list[-1]
    BEST_MODEL_FILE = os.environ["BEST_MODEL_FILE"]
    BEST_MODEL_PATH = os.path.join(MODEL_DIR,BEST_MODEL_DIR, BEST_MODEL_FILE)

    # Extracting the mounted test.csv file
    OUTPUT_FOLDER = '/app/prediction'
    test_file_path = '/app/prediction/test.csv'
    print(f"Testing file path: {test_file_path}")
    df = pd.read_csv(test_file_path)
        
    y_test = df['y']
    X_test = df.drop('y', axis = 1)
   
    print("Shape of the test data")
    print(f"Features = {X_test.shape}")
    print(f"Target = {y_test.shape}")    
    
    print(f"Best Model Path = {BEST_MODEL_PATH}")

    # Load and Run model
    # model = load(BEST_MODEL_PATH)
    with open(BEST_MODEL_PATH, "rb") as file_obj:
        model = dill.load(file_obj)
    print(f"Model Loaded Successfully")
    pred = model.predict(X_test)
    print(f"Model Predicted Successfully")
    rmse = mean_squared_error(y_test, pred, squared=False)
    mae = mean_absolute_error(y_test, pred)
    mape = mean_absolute_percentage_error(y_test, pred)
    r2 = r2_score(y_test, pred)

    # Printing out the metrics
    print("Testing performance")
    print("RMSE: {:.2f}".format(rmse))
    print("MAE: {:.2f}".format(mae))
    print("MAPE: {:.2f}".format(mape))
    print("R2 Score: {:.2f}".format(r2))    

    # Generating the output prediction.csv file
    output_path = os.path.join(OUTPUT_FOLDER, "prediction.csv")
    pred_df = pd.DataFrame(pred, columns=['pred'])
    y_test_df = pd.DataFrame([y_test]).T
    y_df = y_test_df.reset_index()
    test_y_df = y_df.drop('index', axis=1)
    metric_df = test_y_df.join(pred_df)
    metric_df['error'] = abs(round(metric_df['y'] - metric_df['pred'],2))
    metric_df['error%'] = round((metric_df['error']/metric_df['y'])*100,2)

    #Saving the prediction.csv file to the same location as the test.csv file
    metric_df.to_csv(output_path, index=False)
    end = time.time()
    list_lapse = end - start
    print(f"Prediction Time : {str(datetime.timedelta(seconds=list_lapse))}")
    print(f"Prediction output file path : {output_path} ")
    print(f"{'*'*10}Prediction Completed{'*'*10}")
        
   
    
    
if __name__ == '__main__':
    prediction()