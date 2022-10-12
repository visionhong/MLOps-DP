import base64
import json

import click
import grpc
import numpy as np
import requests
import tensorflow as tf
from tensorflow_serving.apis import predict_pb2, prediction_service_pb2_grpc

def read_image(image_file: str="./horse.jpg") -> bytes:
    with open(image_file, "rb") as f:  # 이미지를 바이너리로 read
        raw_image = f.read()
    return raw_image

