FROM tensorflow/tensorflow:2.5.1 as builder

ARG SERVER_DIR=imagenet_inception_v3
ENV PROJECT_DIR synchronous_pattern
WORKDIR /${PROJECT_DIR}
ADD ./${SERVER_DIR}/requirements.txt /${PROJECT_DIR}/

RUN apt-get -y update && \
    apt-get -y install apt-utils gcc && \
    apt-get clean && \  # /var/cache/apt/archives 디렉토리에 다운로드한 파일을 삭제해서 공간확보 \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt

COPY ./${SERVER_DIR}/extract_inception_v3.py /${PROJECT_DIR}/extract_inception_v3.py
COPY ./${SERVER_DIR}/image_net_labels.json /${PROJECT_DIR}/image_net_labels.json

RUN python -m extract_inception_v3.py

FROM tensorflow/serving:2.5.2

ARG SERVER_DIR=imagenet_inception_v3
ENV PROJECT_DIR synchronous_pattern
ENV MODEL_NAME inception_v3
ENV MODEL_BASE_PATH /${PROJECT_DIR}/saved_model/${MODEL_NAME}

COPY --from=builder /${PROJECT_DIR}/saved_model/inception_v3 ${MODEL_BASE_PATH}
EXPOSE 8500
EXPOSE 8501

COPY ./${SERVER_DIR}/tf_serving_entrypoint.sh /usr/bin/tf_serving_entrypoint.sh
RUN chmod +x /usr/bin/tf_serving_entrypoint.sh
ENTRYPOINT ["/usr/bin/tf_serving_entrypoint.sh"]
