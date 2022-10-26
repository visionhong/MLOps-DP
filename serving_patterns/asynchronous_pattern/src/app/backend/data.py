from typing import Any

from pydantic import BaseModel

# 데이터 형식, 타입의 유효성을 검사해 주는 pydantic 즉 Validation Check 라이브러리
# 정의한 타입으로 들어오지 않더라도 정의한 타입으로 자동 변환, Any는 값이 없다면 None으로 채움
class Data(BaseModel):
    image_data: Any


print(Data().dict())
