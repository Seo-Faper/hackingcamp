# Python 베이스 이미지 사용
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 파일 복사
COPY app.py app.py
COPY init.sql init.sql

# 종속성 설치
RUN pip install flask
# Flask 애플리케이션 실행
CMD ["python", "app.py"]

