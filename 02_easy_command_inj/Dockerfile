# Python을 베이스 이미지로 사용
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# Flask 애플리케이션 파일 복사
COPY app.py /app
COPY flag.txt /app

# Flask 설치
RUN pip install flask

# 컨테이너 실행 시 Flask 서버 실행
CMD ["python", "app.py"]

