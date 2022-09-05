import os
from logging import getLogger

from src.constants import CONSTANTS, PLATFORM_ENUM

logger = getLogger(__name__)

class PlatformConfigurations:
    # os.getenv로 컨테이너 환경변수 활용
    platform = os.getenv("PLATFORM", PLATFORM_ENUM.DOCKER.value)  # 왼쪽 값이 존재하면 왼쪽 값을, 존재하지 않으면 오른쪽 값을 가짐.
    if not PLATFORM_ENUM.has_value(platform):  # 인자로 들어오는 값이 PLATFORM_ENUM 클래스의 변수값에 포함 되는지 안되는지 확인
        raise ValueError(f"PLATFORM must be one of {[v.value for v in PLATFORM_ENUM.__members__.values()]}")

class CacheConfigurations:
    cache_host = os.getenv("CACHE_HOST", "redis")
    cache_port = int(os.getenv("CACHE_PORT", 6379))
    queue_name = os.getenv("QUEUE_NAME", "queue")

class RedisCacheConfigurations(CacheConfigurations):
    redis_db = int(os.getenv("REDIS_DB", 0))
    redis_decode_responses = bool(os.getenv("REDIS_DECODE_RESPONSES", True))

class APIConfigurations:
    title = os.getenv('API_TITLE', 'ServingPattern')
    description = os.getenv('API_DESCRIPTION', 'machin learning system serving patterns')
    version = os.getenv('API_VERSION', '0.1')

# Dockerfile에서 설정
class ModelConfigurations:
    model_filepath = os.getenv("MODEL_FILEPATH")
    label_filepath = os.getenv("LABEL_FILEPATH")


logger.info(f"{PlatformConfigurations.__name__}: {PlatformConfigurations.__dict__}")
logger.info(f"{CacheConfigurations.__name__}: {CacheConfigurations.__dict__}")
logger.info(f"{RedisCacheConfigurations.__name__}: {RedisCacheConfigurations.__dict__}")
logger.info(f"{APIConfigurations.__name__}: {APIConfigurations.__dict__}")
logger.info(f"{ModelConfigurations.__name__}: {ModelConfigurations.__dict__}")
