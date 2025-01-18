import sqlite3
from datetime import datetime, timedelta
import random
import os

# 데이터베이스 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 디렉토리
DATABASE_PATH = os.path.join(BASE_DIR, "database.db")  # database.db 파일 경로

# users 테이블 생성 함수
def create_table():
    # 데이터베이스 연결
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # 테이블 생성 쿼리
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        birthdate DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # 테이블 생성 실행
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()
    print("users 테이블이 생성되었습니다.")

# 샘플 데이터 생성 함수
def generate_sample_data():
    # 리그 오브 레전드 챔피언 이름과 성씨 목록
    surnames = ["김", "이", "박", "최", "정", "강", "조", "윤", "장", "임","서","윤","허"]
    names = [
        "아리", "아트록스", "애니", "아무무", "애쉬", "바드", "블리츠크랭크", "브랜드", 
        "카밀", "카서스", "카타리나", "카시오페아", "다리우스", "다이애나", "드레이븐", 
        "이블린", "엘리스", "에코", "피들스틱", "피오라", "피즈", "갈리오", "갱플랭크", 
        "그라가스", "그레이브즈", "그웬", "헤카림", "일라오이", "이렐리아", "아이번", 
        "자르반", "잔나", "자야", "제이스", "진", "징크스", "카이사", "칼리스타", 
        "케인", "케넨", "카직스", "킨드레드", "클레드", "코그모", "르블랑", "리신", 
        "레오나", "릴리아", "리산드라", "루시안", "룰루", "럭스", "말파이트", "말자하", 
        "마스터이", "미스포츈", "모데카이저", "모르가나", "나미", "나서스", "노틸러스", 
        "니코", "니달리", "녹턴", "누누", "올라프", "오리아나", "오른", "오공", 
        "판테온", "파이크", "퀸", "라칸", "라스칼", "라무스", "레넥톤", "렐", "레넥톤"
    ]
    
    data = []
    for i in range(100):
        surname = random.choice(surnames)  # 무작위 성 선택
        name = surname + random.choice(names)  # 성 + 챔피언 이름
        age = random.randint(20, 60)  # 20 ~ 60 사이의 나이
        birthdate = datetime.now() - timedelta(days=age * 365)  # 대략적인 생년월일 계산
        birthdate_str = birthdate.strftime("%Y-%m-%d")
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        data.append((name, age, birthdate_str, created_at))
    
    return data

# 데이터베이스에 데이터 삽입
def insert_sample_data():
    # 데이터베이스 연결
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # 데이터 삽입 쿼리 실행
    try:
        # 예제 데이터 생성
        data = generate_sample_data()
        cursor.executemany("INSERT INTO users (name, age, birthdate, created_at) VALUES (?, ?, ?, ?)", data)
        
        # 커밋
        conn.commit()
        print("100개의 예제 데이터가 삽입되었습니다.")
    
    except sqlite3.Error as e:
        print(f"오류 발생: {e}")
    
    finally:
        # 연결 종료
        conn.close()

# 실행
if __name__ == "__main__":
    create_table()  # 테이블 생성
    insert_sample_data()  # 데이터 삽입
