# 베이스 이미지로 Python 3.9 사용
FROM python:3.9-slim

# 작업 디렉토리를 /app으로 설정
WORKDIR /app

# 로컬 디렉토리의 파일들을 /app으로 복사
COPY . /app

# 필요한 Python 패키지를 설치
RUN pip install --no-cache-dir -r requirements.txt

# Flask 환경 변수를 설정 (Flask 앱 이름과 호스트)
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# 컨테이너에서 25568 포트 개방
EXPOSE 25575

# 애플리케이션을 실행
CMD ["flask", "run", "--host=0.0.0.0", "--port=25575"]
