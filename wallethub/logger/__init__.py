import os
import logging
from wallethub.util.util import log_file_name

LOG_DIR = "WALLETHUB_LOGS"

os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE_NAME = log_file_name()
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)


logging.basicConfig(
    filename = LOG_FILE_PATH,
    filemode= "w",
    format='[%(asctime)s]^;%(levelname)s^;%(filename)s^;%(funcName)s()^;%(lineno)d^;%(message)s',
    level=logging.INFO
)
