import asyncio
import base64
import io
import os
from concurrent.futures import ProcessPoolExecutor
from logging import DEBUG, Formatter, StreamHandler, getLogger
from time import sleep

import grpc
from src.app.backend import request_inception_v3, store_data_job
from src.configurations import CacheConfigurations, ModelConfigurations
from tensorflow_serving.apis import prediction_service_pb2_grpc

log_format = Formatter("%(asctime)s %(name)s [%(levelname)s] %(message)s")
logger = getLogger("prediction_batch")
stdout_handler = StreamHandler()
stdout_handler.setFormatter(log_format)
logger.addHandler(stdout_handler)
logger.setLevel(DEBUG)


# 큐가 존재하면 추론을 실행
def _trigger_prediction_if_queue(stub: prediction_service_pb2_grpc.PredictionServiceStub):
    # queue 에는 job_id만 담고 실제 데이터(이미지)는 redis 에 담음
    job_id = store_data_job.right_pop_queue(CacheConfigurations.queue_name)  # None or job_id
    logger.info(f"predict job_id: {job_id}")
    if job_id is not None:
        data = store_data_job.get_data_redis(job_id)
        if data != "":  # 공백이 아니라면 이미 예측값이 저장되어 있다는 의미
            return True
        # Job id는 있지만 data(추론결과)가 없는 경우는 추론을 수행 해야 함
        image_key = store_data_job.make_image_key(job_id)
        image_data = store_data_job.get_data_redis(image_key)  # 이미지 id로 부터 이미지 취득
        decoded = base64.b64decode(image_data)
        io_bytes = io.BytesIO(decoded)
        prediction = request_inception_v3.request_grpc(
            stub=stub,
            image=io_bytes.read(),
            model_spec_name=ModelConfigurations.model_spec_name,
            signature_name=ModelConfigurations.signature_name,
            timeout_second=5
        )
        if prediction is not None:  # 응답이 성공적으로 오면
            logger.info(f"{job_id} {prediction}")
            store_data_job.set_data_redis(job_id, prediction)  # job id에 예측값 등록
        else:
            store_data_job.left_push_queue(CacheConfigurations.queue_name, job_id)  # 응답이 지연된 경우나 오지 않은 경우 다시 큐에 등록


def _loop():
    serving_address = f"{ModelConfigurations.address}:{ModelConfigurations.grpc_port}"
    channel = grpc.insecure_channel(serving_address)
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)

    while True:
        sleep(1)
        _trigger_prediction_if_queue(stub=stub)


# 멀티 프로세스로 기동
def prediction_loop(num_procs: int=2):
    excutor = ProcessPoolExecutor(num_procs)  # 병렬 연산을 위한 ProcessPoolExecutor
    loop = asyncio.get_event_loop()

    for _ in range(num_procs):
        asyncio.ensure_future(loop.run_in_executor(excutor, _loop()))

    loop.run_forever()

def main():
    NUM_PROCS = int(os.getenv("NUM_PROCS", 2))
    prediction_loop(NUM_PROCS)


if __name__ == '__main__':
    logger.info('start backend')
    main()













