from flask import Flask, request, render_template_string, g
import pymysql
import os

app = Flask(__name__)

# MySQL 접속 정보
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'tjwhdcks1!'
DB_NAME = 'webhacking'

# 데이터베이스 연결 함수
def get_db():
    if not hasattr(g, '_database'):
        g._database = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
    return g._database

# 애플리케이션 종료 시 데이터베이스 연결 닫기
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# 홈 페이지
@app.route('/')
def index():
    return '''
        <h1>우암 던전 입구</h1>
        <h3>SQL Injection Challenge</h3>
        <form method="GET" action="/login">
            <label for="username">Username: </label>
            <input type="text" id="username" name="username" required><br><br>
            <label for="password">Password: </label>
            <input type="password" id="password" name="password" required><br><br>
            <input type="submit" value="Login">
        </form>
    '''

# 로그인 처리 및 SQL 인젝션 시뮬레이션
@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username', '')
    password = request.args.get('password', '')

    # 취약한 SQL 쿼리 생성
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

    # 사용자 입력 부분을 하이라이팅
    highlighted_query = query.replace(f"{username}", f"<span style='color: red;'>{username}</span>")
    highlighted_query = highlighted_query.replace(f"{password}", f"<span style='color: red;'>{password}</span>")

    # SQL 쿼리 실행
    db = get_db()
    try:
        with db.cursor() as cursor:
            cursor.execute(query)
            result_set = cursor.fetchall()

        if result_set:
            result = "Login successful!"
        else:
            result = "Login failed!"
    except pymysql.Error as err:
        result = f"Error: {err}"

    # 결과 출력
    return render_template_string(f'''
        <h1>우암 던전 입구</h1>
        <h3>SQL Injection Challenge</h3>
        <form method="GET" action="/login">
            <label for="username">Username: </label>
            <input type="text" id="username" name="username" required><br><br>
            <label for="password">Password: </label>
            <input type="password" id="password" name="password" required><br><br>
            <input type="submit" value="Login">
        </form>
        <p>{result}</p>
        <h4>Executed Query:</h4>
        <p>{highlighted_query}</p>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=25576)
