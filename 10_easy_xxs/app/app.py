from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets
from datetime import datetime, timedelta  
import re


app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'ctf_board.db')

# SQLite 연결
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# 데이터베이스 초기화
def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL,
                        is_admin INTEGER DEFAULT 0 
                    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS posts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        title TEXT NOT NULL,     
                        content TEXT NOT NULL,   
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS comments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        post_id INTEGER NOT NULL,
                        user_id INTEGER NOT NULL,
                        content TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (post_id) REFERENCES posts (id),
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )''')
    conn.commit()
    conn.close()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  # 자동 설치
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
@app.route('/admin_notify/<int:post_id>', methods=['POST'])
def admin_notify(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT id, title FROM posts WHERE id = ?', (post_id,)).fetchone()

    if not post:
        flash("게시글을 찾을 수 없습니다.", "error")
        return redirect(url_for('home'))

    try:
        # Selenium WebDriver 설정
        options = Options()
        # options.add_argument('--headless')  # 필요 시 백그라운드 실행
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')

        # ChromeDriver 자동 설치 및 WebDriver 초기화
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # 관리자 로그인 페이지 접속
        driver.get('http://localhost:25575/login')

        # 로그인 폼에 관리자 계정 정보 입력
        driver.find_element(By.NAME, 'username').send_keys('admin')
        driver.find_element(By.NAME, 'password').send_keys('tjwhdcks1!')
        driver.find_element(By.NAME, 'password').submit()

        # 관리자 세션에 플래그 쿠키 추가
        driver.add_cookie({'name': 'flag', 'value': 'cbcamp{MY_ADMIN_FLAG_FOR_XSS!!}'})
        print(driver.get_cookies())
        # 특정 게시글로 이동
        driver.get(f'http://localhost:25575/post/{post_id}')

        try:
            alert = driver.switch_to.alert
            print(f"Alert Text: {alert.text}")  
            alert.accept()  
            print("Alert 처리 완료")
        except NoAlertPresentException:
            print("Alert이 없습니다.")

        # 댓글 작성
        comment_box = driver.find_element(By.NAME, 'comment')  # 댓글 입력 필드 찾기
        comment_box.clear()
        comment_box.send_keys("조치완료했습니다")  # 댓글 입력

        # 버튼 활성화 확인 및 클릭
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[name="comment_to_submit"]')
        if not submit_button.is_enabled():
            # JavaScript로 버튼 활성화
            driver.execute_script("arguments[0].removeAttribute('disabled');", submit_button)
        submit_button.click()  # 댓글 제출

        print(f"관리자가 게시글 {post_id}에 댓글을 남겼습니다.")

    except UnexpectedAlertPresentException as e:
        print(f"Selenium 에러: Alert Text: {e.alert_text}")
    except Exception as e:
        print(f"Selenium 에러: {e}")
    finally:
        driver.quit()

    conn.close()
    return redirect(url_for('post_detail', post_id=post_id))


def is_admin():
    if 'user_id' in session:
        conn = get_db_connection()
        user = conn.execute('SELECT is_admin FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        conn.close()
        if user and user['is_admin'] == 1:
            session['is_admin'] = True  # 세션에 관리자 권한 저장
            return True
    return False

# 홈 페이지 (로그인 여부에 따라 다르게 표시)
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # 로그인하지 않은 경우 로그인 페이지로 리다이렉트

    conn = get_db_connection()
    # 모든 사용자는 모든 게시글의 목록을 볼 수 있음
    posts = conn.execute('''
        SELECT posts.id, posts.title, users.username, posts.created_at 
        FROM posts
        JOIN users ON posts.user_id = users.id
    ''').fetchall()
    conn.close()

    return render_template('home.html', posts=posts)

# 회원가입
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        
        # 사용자명이 이미 존재하는지 확인
        existing_user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if existing_user:
            flash('이미 존재하는 사용자명입니다. 다른 이름을 사용해주세요.', 'error')
            conn.close()
            return redirect(url_for('signup'))
        
        # 'admin' 사용자의 경우 is_admin 값을 1로 설정
        is_admin = 1 if username.lower() == 'admin' else 0

        # 새로운 사용자 추가
        conn.execute('INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)', 
                     (username, hashed_password, is_admin))
        conn.commit()
        conn.close()

        flash('회원가입 성공! 로그인해주세요.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')
# 로그인
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('home'))
        else:
            flash('잘못된 사용자명 또는 비밀번호입니다.')
    
    return render_template('login.html')

# 로그아웃
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('로그아웃되었습니다.')
    return redirect(url_for('home'))

# 게시글 작성
@app.route('/post', methods=['GET', 'POST'])
def post():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # 게시글 작성 쿨타임 (15초)
    last_post_time = session.get('last_post_time')
    current_time = datetime.now()

    if last_post_time:
        # 마지막 게시글 작성 시간과 현재 시간의 차이를 계산
        time_diff = current_time - datetime.strptime(last_post_time, '%Y-%m-%d %H:%M:%S')
        if time_diff < timedelta(seconds=15):
            remaining_time = 15 - time_diff.seconds
            flash(f"새로운 게시글은 {remaining_time}초 후에 작성할 수 있습니다.", "warning")
            return redirect(url_for('home'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)', 
                     (session['user_id'], title, content))
        conn.commit()
        conn.close()

        # 현재 게시글 작성 시간을 세션에 저장
        session['last_post_time'] = current_time.strftime('%Y-%m-%d %H:%M:%S')

        flash('게시글 작성 완료!', 'success')
        return redirect(url_for('home'))
    
    return render_template('post.html')

# 게시글 상세 페이지
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    # 'bot_token'이 전달된 경우, 세션 없이 접근 허용
    bot_token = request.args.get('bot_token')
    if bot_token != "your_bot_token" and 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    post = conn.execute('''
        SELECT posts.id, posts.title, posts.content, posts.created_at, users.username, posts.user_id
        FROM posts
        JOIN users ON posts.user_id = users.id
        WHERE posts.id = ?
    ''', (post_id,)).fetchone()

    # 댓글 가져오기
    comments = conn.execute('''
        SELECT comments.content, comments.created_at, users.username
        FROM comments
        JOIN users ON comments.user_id = users.id
        WHERE comments.post_id = ?
        ORDER BY comments.created_at
    ''', (post_id,)).fetchall()

    if request.method == 'POST':
        # 봇 접근 시에는 세션 체크 없이 댓글 작성 가능
        if bot_token != "your_bot_token" and not is_admin():
            flash('관리자만 댓글을 달 수 있습니다.')
            return redirect(url_for('post_detail', post_id=post_id))

        comment_content = request.form['comment']
        user_id = session.get('user_id', 1) if bot_token == "your_bot_token" else session['user_id']
        conn.execute('INSERT INTO comments (post_id, user_id, content) VALUES (?, ?, ?)', 
                     (post_id, user_id, comment_content))
        conn.commit()
        return redirect(url_for('post_detail', post_id=post_id))

    conn.close()

    # 관리자는 모든 게시글 조회 가능, 일반 사용자는 자신의 게시글만 조회 가능
    if post is None or (not is_admin() and post['user_id'] != session.get('user_id')):
        flash('오직 본인의 게시글만 볼 수 있습니다.')
        return redirect(url_for('home'))

    return render_template('post_detail.html', post=post, comments=comments, is_admin=is_admin())


if __name__ == '__main__':
    init_db() 
    app.run(host='0.0.0.0', port=25575)
