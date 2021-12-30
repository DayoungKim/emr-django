Required
--------
python 3.8
pip
virtualenv
docker
docker-compose

Operation
---------
python library 설치
특정 버전, directory의 python 사용 원하는 경우 Makefile의 MOTHER_PYTHON 수정
수정예시 : MOTHER_PAYHON ?= /dir/to/python_you_want/bin/python

    make venv

로컬 환경에 celery 설치
원격의 celery 사용시 server.env 파일의 REDIS_HOST 변수 수정
다음의 명령어로 redis 설치

    make redis

server.env 파일에 적절한 값 입력하기
다음의 명령어로 환경변수 적용하기

    source server.env

서버 실행

    make server


APIs
----
[swagger](http://localhost:8000/swagger/) 로 접속하여 api를 확인하세요
