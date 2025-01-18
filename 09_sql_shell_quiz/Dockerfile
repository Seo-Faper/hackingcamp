# 베이스 이미지로 Python 사용
FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /app

# Flask 애플리케이션 파일 복사
COPY app.py /app
COPY databases.db /app
# 필요한 패키지 설치
RUN pip install flask sqlite3 tabulate

# 8000 포트 노출
EXPOSE 8000

# Flask 애플리케이션 실행
CMD ["python", "app.py"]
