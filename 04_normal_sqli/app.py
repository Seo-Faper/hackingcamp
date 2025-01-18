from flask import Flask, request, render_template_string, g
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'database.db'

# 데이터베이스 연결 함수
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # 쿼리 결과를 딕셔너리처럼 사용
    return db

# 애플리케이션 종료 시 데이터베이스 연결 닫기
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# 초기화 스크립트 실행
def init_db():
    with app.app_context():
        db = get_db()
        with open('init.sql', 'r') as f:
            db.executescript(f.read())

# 홈 페이지
@app.route('/')
def index():
    return '''
        <h1>우암 던전 입구</h1>
        <h3></h3>
        <h3>query: SELECT * from users WHERE username = '?' AND password ='?'</h3>
        <form method="POST" action="/login">
            <label for="username">Username: </label>
            <input type="text" id="username" name="username" required><br><br>
            <label for="password">Password: </label>
            <input type="password" id="password" name="password" required><br><br>
            <input type="submit" value="Login">
        </form>
    '''

# 로그인 처리 및 SQL 인젝션 시뮬레이션
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # 취약한 SQL 쿼리 생성
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

    # 하이라이팅: 사용자 입력 부분을 따옴표와 함께 정확하게 하이라이팅
    highlighted_query = query.replace(f"{username}", f"<span style='color: red;'>{username}</span>")
    highlighted_query = highlighted_query.replace(f"{password}", f"<span style='color: red;'>{password}</span>")

    # SQL 쿼리 실행
    db = get_db()
    try:
        cursor = db.execute(query)
        result_set = cursor.fetchall()

        if result_set:
            result = "Login successful! FLAG is cbcamp{SQL_INJec7iOn_CHall}"
        else:
            result = "Login failed!"
    except sqlite3.Error as err:
        result = f"Error: {err}"

    # 결과 출력
    return render_template_string(f'''
        <h1>SQL Injection Challenge</h1>
        <h3>query: {highlighted_query}</h3>
        <form method="POST" action="/login">
            <label for="username">Username: </label>
            <input type="text" id="username" name="username" required><br><br>
            <label for="password">Password: </label>
            <input type="password" id="password" name="password" required><br><br>
            <input type="submit" value="Login">
        </form>
        <p>{result}</p>
    ''')

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()  # 데이터베이스 초기화
    app.run(host='0.0.0.0', port=25568)

