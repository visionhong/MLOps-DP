FROM python:3.8-slim

ENV PROJECT_DIR model_in_image_pattern
WORKDIR /${PROJECT_DIR}
ADD ./requirements.txt /${PROJECT_DIR}/
RUN apt-get -y update && \
    apt-get -y install apt-utils gcc curl && \
    pip install --no-cache-dir -r requirements.txt  # docker image
# apt-get update: 설치가능한 패키지들과 그 버전에 대한 정보를 업데이트
# --no-cache-dir: 하드디스크 용량절약 및 이미지 크기 축소

COPY ./src/ /${PROJECT_DIR}/src/
COPY ./models/ /${PROJECT_DIR}/models/

# 컨테이너에서 활용할 환경변수 설정
ENV MODEL_FILEPATH /${PROJECT_DIR}/models/iris_svc.onnx
ENV LABEL_FILEPATH /${PROJECT_DIR}/models/label.json
ENV LOG_LEVEL DEBUG
ENV LOG_FORMAT TEXT

COPY ./run.sh /${PROJECT_DIR}/run.sh
RUN chmod +x /${PROJECT_DIR}/run.sh
CMD ["./run.sh"]

