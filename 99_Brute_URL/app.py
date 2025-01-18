from flask import Flask, render_template_string, abort

app = Flask(__name__)

# 정답 플래그
FLAG = "CBCAMP{WOOAM}"

# 경로를 확인하는 함수
def is_correct_path(path_parts):
    flag_parts = list(FLAG)
    if len(path_parts) > len(flag_parts):
        return False
    for i, part in enumerate(path_parts):
        if part != flag_parts[i]:
            return False
    return True

@app.route('/<path:subpath>', methods=['GET'])
def brute_force_handler(subpath):
    path_parts = subpath.split('/')
    if is_correct_path(path_parts):
        if len(path_parts) == len(FLAG):
            return render_template_string(TEMPLATE, message=f"Congratulations! The flag is <span style='color: white;'>{FLAG}</span>")
        return render_template_string(TEMPLATE, message=f"Correct up to: <span style='color: white;'>{''.join(path_parts)}</span>")
    else:
        abort(404)

@app.route('/')
def home():
    return render_template_string(TEMPLATE, message="""
        <h2>우암던전 100층에 도달했습니다.</h2>
        <p>노력은 배신하지 않는다. <span style='color: #121212;'>사실 할수도있다. 플래그는 모두 대문자, {}_ 으로만 이뤄져 있다. CBCAMP{로 시작한다는 뜻이다.</span></p>
        <p>난 충분한 힌트를 줬다.</p>
        <span style='color: #121212;'>hint : url : /C/B/C/A/M/P{</span>
    """)

# 공통 HTML 템플릿
TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>우암던전</title>
    <style>
        body {
            background-color: #121212; /* 어두운 배경 */
            color: #e0e0e0; /* 밝은 텍스트 */
            font-family: "Courier New", Courier, monospace; /* 판타지 분위기 폰트 */
            text-align: center;
            margin: 0;
            padding: 0;
        }
        h1, h2 {
            margin: 20px 0;
            color: #f39c12; /* 황금색 텍스트 */
        }
        p {
            margin: 10px 0;
            font-size: 18px;
        }
        .hint {
            color: #ffffff;
            font-size: 14px;
        }
        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }
        .box {
            border: 3px solid #f39c12; /* 황금 테두리 */
            padding: 20px;
            width: 60%;
            border-radius: 10px;
            background-color: #1c1c1c; /* 어두운 상자 */
            box-shadow: 0 0 10px #f39c12; /* 황금빛 발광 */
        }
        .hidden-text {
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="box">
            <h1>우암던전</h1>
            {{ message | safe }}
        </div>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=25576)
