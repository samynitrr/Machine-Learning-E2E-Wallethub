from wallethub.pipeline.pipeline import Pipeline
from wallethub.get_config.configuration import Configuration
from wallethub.constants import CONFIG_FILE_PATH
from wallethub.logger import logging
from wallethub.util.util import get_current_time_stamp
def main():
    try:
        pipeline = Pipeline(config=Configuration(current_time_stamp=get_current_time_stamp()))

        if not Pipeline.experiment.running_status:
            message = "Training started."
            logging.info(f"Training started.")
            print(message)
            pipeline.start()
        else:
            message = "Training is already in progress."
            logging.info(f"Training is already in progress.")
            print(message)
            pipeline.start()
            
    except Exception as e:
        logging.error(f"{e}")
        print(e)       


if __name__ == "__main__":
    main()






