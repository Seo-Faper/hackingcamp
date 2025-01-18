# Python 3 베이스 이미지 사용
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 로컬의 index.html과 game.js 파일을 도커 이미지로 복사
COPY index.html /app
COPY game.js /app

# Python의 간단한 HTTP 서버로 index.html 제공
CMD ["python3", "-m", "http.server", "80"]
