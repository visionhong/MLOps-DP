FROM python:3.8-slim

ENV PROJECT_DIR model_load_pattern

WORKDIR /${PROJECT_DIR}
COPY ./model_loader/requirements.txt /${PROJECT_DIR}/
COPY ./model_loader/main.py /${PROJECT_DIR}/src/main.py

#COPY ./model_loader/model-magnet-358500-c938d952b597.json /${PROJECT_DIR}/
#ENV GOOGLE_APPLICATION_CREDENTIALS /${PROJECT_DIR}/model-magnet-358500-c938d952b597.json

RUN apt-get -y update && \
    apt-get -y install apt-utils gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt
