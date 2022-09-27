from logging import getLogger
from typing import Dict, List

from fastapi import APIRouter
from src.ml.prediction import Data, classifier

logger = getLogger(__name__)
router = APIRouter()


@router.get('/health')
def health() -> Dict[str, str]:
    return {'health': 'ok'}

@router.get('/metadata')
def metadata():
    return {
        'data_type': 'float32',
        'data_structure': '(1,4)',
        'data_sample': Data().data,  # [[5.1, 3.5, 1.4, 0.2]]
        'prediction_type': 'float32',
        'prediction_structure': "(1, 3)",  # 3 classes
        'prediction_sample': [0.971, 0.015, 0.014],
    }

@router.get('/label')
def label():
    return classifier.label  # Classifier 클래스의 self.label은 초기화 과정에서 이미 load_label() 함수를 실행

# 샘플 데이터로 predict test를 진행하는 router
@router.get('/predict/test')
def predict_test() -> Dict[str, List[float]]:
    prediction = classifier.predict(data=Data().data)
    return {'prediction': list(prediction)}

@router.get('/predict/test/label')
def predict_test_label() -> Dict[str, str]:
    prediction = classifier.predict_label(data=Data().data)
    return {'predictiom': prediction}

# 입력 데이터를 predict
@router.post('/predict')
def predict(data: Data) -> Dict[str, List[float]]:
    prediction = classifier.predict(data=data.data)
    return {'prediction': list(prediction)}

@router.post('/predict/label')
def predict_label(data:Data) -> Dict[str, str]:
    prediction = classifier.predict_label(data=data.data)
    return {'prediction': prediction}
