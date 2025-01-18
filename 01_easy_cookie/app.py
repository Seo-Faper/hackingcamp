from flask import Flask, request, make_response, render_template_string, Response

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # 세션 키는 필요하지 않음
app.config['JSON_AS_ASCII'] = False

FLAG = "cbcmap{01_쿠키와_세션_실습}"
successful_users = []  # 모든 사용자들이 공유할 리스트

# HTML 템플릿: JavaScript prompt로 이름을 입력받고 성공 리스트 표시
html_template = """
    <meta charset="UTF-8">
    <script>
        // 쿠키에서 name을 확인하고, 없으면 prompt를 띄움
        function getCookie(name) {
            let value = "; " + document.cookie;
            let parts = value.split("; " + name + "=");
            if (parts.length == 2) return parts.pop().split(";").shift();
        }

        // 유효한 이름을 입력할 때까지 반복해서 이름을 물어봄
        var name = getCookie('name');
        while (!name || name.trim() === '' || name == 'null' || name == 'undefined') {
            name = prompt("Enter your name (cannot be empty):");
        }

        // 이름이 유효하면 쿠키에 저장하고 서버로 전송
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
    </script>
    <center>
        <h2>Welcome {{ name }}!</h2>

        <p>{{ role_message }}</p>
        <h3>실습에 성공한 사람들</h3>
        <table border="1" cellpadding="5" cellspacing="0">
            <thead>
                <tr>
                    <th>No.</th>
                    <th>이름</th>
                </tr>
            </thead>
            <tbody>
            {% for idx, user in enumerate(successful_users, 1) %}
                <tr>
                    <td>{{ idx }}</td>
                    <td>{{ user }}</td>
                </tr>
            {% endfor %}
            </tbody>
        </table>
    <center>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    global successful_users  # 전역 리스트 사용

    if request.method == 'POST':
        # POST 요청으로 이름을 입력받음
        name = request.form.get('name')

    # 쿠키에서 사용자 이름 가져오기 (없으면 guest로 설정)
    name = request.cookies.get('name', 'guest')

    # 쿠키에서 role 가져오기
    role = request.cookies.get('role')

    # 최초 접속 시 role이 없으면 user로 설정
    if not role:
        role = 'user'
        rendered_template = render_template_string(html_template, name=name, role_message="Your role is NOT admin.", successful_users=successful_users, enumerate=enumerate)
        resp = make_response(rendered_template)
        resp.set_cookie('role', 'user')
        resp.headers["Content-Type"] = "text/html; charset=utf-8"  # 인코딩 설정
        return resp

    # role이 admin이면 플래그 제공
    if role == 'admin':
        if name and name not in successful_users:
            successful_users.append(name)
        rendered_template = render_template_string(html_template, name=name, role_message=f"Welcome Admin, flag is: {FLAG}", successful_users=successful_users, enumerate=enumerate)
        return Response(rendered_template, content_type="text/html; charset=utf-8")
    
    # 기본 role은 user
    rendered_template = render_template_string(html_template, name=name, role_message="Your role is NOT admin.", successful_users=successful_users, enumerate=enumerate)
    return Response(rendered_template, content_type="text/html; charset=utf-8")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=25565)
