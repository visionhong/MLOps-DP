import base64
import io
import uuid
from logging import getLogger
from typing import Any, Dict

import requests
from fastapi import APIRouter, BackgroundTasks
from PIL import Image
from src.app.backend import background_job, store_data_job
from src.app.backend.data import Data
from src.configurations import ModelConfigurations

logger = getLogger(__name__)
router = APIRouter()

# health check
@router.get("/health")
def health() -> Dict[str, str]:
        return {"health", "ok"}


# 모델에 대한 metadata를 TF Serving에 get 요청
@router.get("/metadata")
def metadata() -> Dict[str, Any]:
    model_spec_name = ModelConfigurations.model_spec_name
    address = ModelConfigurations.address
    port = ModelConfigurations.rest_port
    serving_address = f"http://{address}:{port}/v1/models/{model_spec_name}/versions/0/metadata"  # TFServing 엔드포인트 규칙
    response = requests.get(serving_address)
    return response.json()


# 라벨 인덱스와 값을 return
@router.get('/label')
def label() -> Dict[int, str]:
    return ModelConfigurations.labels


@router.get('/predict/test')
def predict_test(background_tasks: BackgroundTasks) -> Dict[str, str]:
    job_id = str(uuid.uuid4())[:6]
    data = Data()
    data.image_data = ModelConfigurations.sample_image
    background_job.save_data_job(data.image_data, job_id, background_tasks, True)
    return {'job_id': job_id}


# 이미지를 redis에 새로 등록 -> 추론은 background에서 이미 loop를 돌면서 추론중
@router.get('/predict')
def predict(data: Data, background_tasks: BackgroundTasks) -> Dict[str, str]:
    image = base64.b64decode(str(data.image_data))
    io_bytes = io.BytesIO(image)
    data.image_data = Image.open(io_bytes)
    job_id = str(uuid.uuid4())[:6]
    background_job.save_data_job(
        data=data.image_data,
        job_id=job_id,
        background_tasks=background_tasks,
        enqueue=True
    )
    return {'job_id': job_id}


# 해당 job의 결과값 get
@router.get("/job/{job_id}")
def prediction_result(job_id: str) -> Dict[str, Dict[str, str]]:
    result = {job_id: {'prediction': ""}}
    data = store_data_job.get_data_redis(job_id)
    result[job_id]["prediction"] = data
    return result


























