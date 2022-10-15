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


@router.get("/predict/test")
def predict_test(background_tasks)
