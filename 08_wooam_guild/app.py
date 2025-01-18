from flask import Flask, request, make_response, render_template_string, jsonify

app = Flask(__name__)
app.secret_key = 'supersecretkey'

FLAG = "CBCAMP{welcome_to_wooam_gu!1d}"
successful_users = []
recommend_counts = {}  # 각 사용자별 추천 수를 저장하는 딕셔너리

# HTML 템플릿
html_template = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>추천 시스템</title>
    </head>
    <body>
        <script>
        let rank = 1;
            function getCookie(name) {
                let value = "; " + document.cookie;
                let parts = value.split("; " + name + "=");
                if (parts.length == 2) return parts.pop().split(";").shift();
            }

            var name = getCookie('name');
            while (!name || name.trim() === '' || name == 'null' || name == 'undefined') {
                name = prompt("Enter your name (cannot be empty):");
            }

            if (name) {
                document.cookie = "name=" + name;
                fetch("/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    body: "name=" + encodeURIComponent(name)
                }).then(response => response.text())
                  .then(data => document.body.innerHTML = data);
            }

            // 추천 수 관리
            function recommend(userIdx) {
                if (getCookie("recommended_" + userIdx) === "true") {
                    alert("이미 추천한 사용자 입니다.");
                    return;
                }
                document.cookie = "recommended_" + userIdx + "=true";
                
                let increaseAmount = rank;
                let recommendCountElement = document.getElementById("recommend-count-" + userIdx);
                let currentCount = parseInt(recommendCountElement.innerText) || 0;
                recommendCountElement.innerText = currentCount + increaseAmount;

                // 백엔드에 추천 업데이트 전송
                fetch("/recommend", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    body: "user_idx=" + encodeURIComponent(userIdx) + "&count=" + increaseAmount
                }).then(response => response.json())
                  .then(data => {
                      document.body.innerHTML = data.html;  // 새 HTML 응답으로 업데이트
                      if (data.showAlert) {
                          alert("Congratulations! Flag: {{ FLAG }}");
                      }
                  });
            }
        </script>
        <center>
            <h3>우암 길드 현황판</h3>
            <table border="1" cellpadding="5" cellspacing="0">
                <thead>
                    <tr>
                        <th>No.</th>
                        <th>이름</th>
                        <th>추천수</th>
                        <th>추천하기</th>
                    </tr>
                </thead>
                <tbody>
                {% for idx, user in enumerate(successful_users, 1) %}
                    <tr>
                        <td>{{ idx }}</td>
                        <td>{{ user }}</td>
                        <td id="recommend-count-{{ idx }}">{{ recommend_counts.get(user, 0) }}</td> <!-- 백엔드에서 관리하는 추천 수 표시 -->
                        <td><button onclick="recommend({{ idx }})">추천하기</button></td>
                    </tr>
                {% endfor %}
                </tbody>
            </table>
        </center>
    </body>
    </html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    global successful_users  # 전역 변수 사용

    if request.method == 'POST':
        name = request.form.get('name')
        if name and name not in successful_users:
            successful_users.append(name)

    name = request.cookies.get('name', 'guest')

    response = make_response(render_template_string(
        html_template,
        name=name,
        successful_users=successful_users,
        FLAG=FLAG,
        recommend_counts=recommend_counts,
        enumerate=enumerate
    ))
    response.headers["Content-Type"] = "text/html; charset=utf-8"  # UTF-8 설정
    return response

@app.route('/recommend', methods=['POST'])
def recommend():
    user_idx = request.form.get('user_idx')
    increase_count = int(request.form.get('count', 1))  # 프론트엔드에서 전달한 증가량
    showAlert = False  # 플래그 표시 여부 초기화

    # 현재 사용자 이름을 쿠키에서 가져옴
    current_user_name = request.cookies.get('name', 'guest')

    if user_idx:
        user_idx = int(user_idx) - 1  # 인덱스 조정
        if 0 <= user_idx < len(successful_users):
            user_name = successful_users[user_idx]
            
            # 추천 수 증가
            recommend_counts[user_name] = recommend_counts.get(user_name, 0) + increase_count

            # 자기 자신에게만 플래그 표시 조건 적용
            if user_name == current_user_name and recommend_counts[user_name] >= 100:
                showAlert = True

    # 최신 HTML 응답 생성
    updated_html = render_template_string(
        html_template,
        name=current_user_name,
        successful_users=successful_users,
        FLAG=FLAG,
        recommend_counts=recommend_counts,
        enumerate=enumerate
    )
    
    return jsonify({"showAlert": showAlert, "html": updated_html})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=25570)
