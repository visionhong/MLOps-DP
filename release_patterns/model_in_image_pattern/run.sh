#!/bin/bash

set -eu
# -e: 옵션은 아래 명령어들을 실행하다가 실패하게되면 곧바로 script의 실행이 멈추게 됨.
# -u: 설정되지 않은 변수를 오류로 처리

# :- : default value
HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-8000}
WORKERS=${WORKERS:-4}
UVICORN_WORKER=${UCIVORN_WORKER:-"uvicorn.workers.UvicornWorker"}
LOGLEVEL=${LOGLEVEL:-"debug"}
LOGCONFIG=${LOGCONFIG:-"./src/utils/logging.conf"}
BACKLOG=${BACKLOG:-2048}
LIMIT_MAX_REQUESTS=${LIMIT_MAX_REQUESTS:-65536}
MAX_REQUESTS_JITTER=${MAX_REQUESTS_JITTER:-2048}
GRACEFUL_TIMEOUT=${GRACEFUL_TIMEOUT:-10}
APP_NAME=%{APP_NAME:-"src.app.app:app"}

# gunicorn(green unicorn) = WSGI(Web Server Gateway Interface)
# - python으로 작성된 웹 어플리케이션과 python으로 작성된 서버 사이의 약속된 인터페이스 또는 규칙
# 첫번째 인자: wsgi app
# -b: 바인딩 할 서버 소켓
# -w: worker 프로세스 수. 일반적으로 서버의 코어당 2-4개를 사용
# -k: 실행할 worker 프로세스의 타입.
# --log-level: 오류 로그 출력의 세분성
# --log-config: 사용할 로그 구성 파일. gnicorn은 python 로깅 모듈의 구성 파일 형식을 사용
# --backlog: 서비스를 대기할 수 있는 클라이언트의 수. 이 수를 초과하면 연결을 시도할 때 클라이언트에 오류가 발생. 일반적으로 64~2048 범위에서 설정
# --max-requests: 0보다 큰 값은 worker가 자동으로 재시작하기 전에 처리할 요청 수를 제한한다. 최대 요청 수를 제한함으로써 메모리 누수 피해를 줄임
# --max-requests-jitter: 모든 worker가 동식에 다시 시작되지 않도록 0에서 설정한 값 사이 랜덤값으로 지정된다.
# --graceful-timeout: timeout되어 재시작된 worker를 강제 종료
# --reload: 코드가 변경되면 변경된 코드로 재실행

gunicorn ${APP_NAME} \
    -b ${HOST}:${PORT} \
    -w ${WORKERS} \
    -k ${UVICORN_WORKER} \
    --log-level ${LOGLEVEL} \
    --log-config ${LOGCONFIG} \
    --backlog ${BACKLOG} \
    --max-requests ${LIMIT_MAX_REQUESTS} \
    --max-requests-jitter ${MAX_REQUESTS_JITTER} \
    --graceful-timeout ${GRACEFUL_TIMEOUT} \
    --reload
