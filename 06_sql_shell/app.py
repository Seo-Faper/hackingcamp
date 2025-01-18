from flask import Flask, render_template, request
import sqlite3
import io
import os
from tabulate import tabulate

app = Flask(__name__)

# 데이터베이스 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # app.py가 있는 디렉토리
DATABASE_PATH = os.path.join(BASE_DIR, "database.db")  # database.db의 절대 경로

# 데이터베이스 연결 함수
def execute_sql(query):
    output = io.StringIO()  # CLI 결과 형식을 위해 StringIO 사용
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:  # 절대 경로로 연결
            cursor = conn.cursor()

            # 여러 개의 쿼리를 ';'로 분리하여 실행
            statements = query.split(';')
            for statement in statements:
                statement = statement.strip()
                if statement:  # 빈 문자열이 아닐 경우에만 실행
                    cursor.execute(statement)

                    # SELECT 쿼리인 경우
                    if statement.lower().startswith("select"):
                        columns = [description[0] for description in cursor.description]
                        rows = cursor.fetchall()
                        
                        # 테이블 형태로 출력
                        table = tabulate(rows, headers=columns, tablefmt="grid")
                        output.write(table + "\n")
                    else:
                        # 데이터 변경 SQL 명령어인 경우 커밋 및 성공 메시지 출력
                        conn.commit()
                        output.write("명령어가 성공적으로 실행되었습니다.\n")
                
    except sqlite3.Error as e:
        output.write(f"ERROR: {e}\n")
    
    # CLI와 유사한 출력 형식의 텍스트 반환
    return output.getvalue()

# SQL 쉘 페이지
@app.route('/')
def shell():
    return render_template('shell.html')

# SQL 실행 API 엔드포인트
@app.route('/execute', methods=['POST'])
def execute():
    query = request.form.get('query')
    result = execute_sql(query)
    return result, 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == '__main__':
    app.run(debug=True)
