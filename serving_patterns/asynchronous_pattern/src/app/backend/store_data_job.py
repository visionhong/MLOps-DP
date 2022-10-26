import base64
import io
import json
import logging
from typing import Any, Dict

import numpy as np
from PIL import Image
from src.app.backend.redis_client import redis_client

logger = logging.getLogger(__name__)

# 큐에 등록할 키 작성
def make_image_key(key: str) -> str:
    return f"{key}_image"

# 큐 등록
def left_push_queue(queue_name: str, key: str) -> bool:
    try:
        redis_client.lpush(queue_name, key)
        return True
    except Exception:
        return False

# 큐 취득
def right_pop_queue(queue_name: str) -> Any:
    if redis_client.llen(queue_name) > 0:
        return redis_client.rpop(queue_name)
    else:
        return None

# Redis에 데이터 등록
def set_data_redis(key: str, value: str) -> bool:
    redis_client.set(key, value)
    return True

# Redis로부터 데이터 취득
def get_data_redis(key: str) -> Any:
    data = redis_client.get(key)
    return data

# Redis에 이미지 데이터 등록
def set_image_redis(key:str, image: Image.Image) -> str:
    byte_io = io.BytesIO()
    image.save(byte_io, format=image.format)
    image_key = make_image_key(key)
    encoded = base64.b64encode(byte_io.getvalue())
    redis_client.set(image_key, encoded)
    return image_key

# Redis로부터 이미지 데이터 취득
def get_image_redis(key:str) -> Image.Image:
    redis_data = redis_client.get(key)
    decoded = base64.b64decode(redis_data)
    io_bytes = io.BytesIO(decoded)
    image = Image.open(io_bytes)
    return image

# Redis에 데이터와 작업 ID 등
def save_image_redis_job(job_id: str, image: Image.Image) -> bool:
    set_image_redis(job_id, image)
    redis_client.set(job_id, "")
    return True
