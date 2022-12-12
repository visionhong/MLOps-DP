import asyncio
import logging
import os
import uuid
from typing import Any, Dict, List

import httpx
from fastapi import APIRouter
from pydantic import BaseModel
from src.api_composition_proxy.configurations import ServiceConfigurations

logger = logging.getLogger(__name__)

router = APIRouter()

class Data(BaseModel):
    data: List[List[float]] = [[5.1, 3.5, 1.4, 0.2]]

@router.get("/health")
def health() -> Dict[str, str]:
    return {"health": "ok"}


@router.get("/metadata")
def metadata() -> Dict[str, Any]:
    return {
        "data_type": "float32",
        "data_structure": "(1,4)",
        "data_sample": Data().data,
        "prediction_type": "float32",
        "prediction_structure": "(1,2)",
        "prediction_sample": {
            "service_setosa": [0.970000, 0.030000],
            "service_versicolor": [0.970000, 0.030000],
            "service_virginica": [0.970000, 0.030000],
        },
    }

@router.get("/health/all")
async def health_all() -> Dict[str, Any]:
    logger.info(f"GET redirect to: /health")
    results = {}
    async with httpx.AsyncClient() as ac:
        async def req(ac, service, url):
            response = await ac.get(f"{url}/health")
            return service, response

        # 각 추론기의 health check
        tasks = [req(ac, service, url) for service, url in ServiceConfigurations.services.items()]
























