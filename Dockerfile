FROM python:3.7-slim

COPY model_registry /app/model_registry
COPY wallethub /app/wallethub
COPY prediction.py /app/prediction.py
COPY requirements.txt /app/requirements.txt

WORKDIR /app

ENV MODEL_DIR=/app/model_registry
ENV BEST_MODEL_FILE=model.pkl

RUN python -m pip install xgboost requests PyYaml dill pandas scikit-learn


CMD [ "python" , "/app/prediction.py"]