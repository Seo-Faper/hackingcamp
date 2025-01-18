import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

FLAG_PATH = './flag.txt'
FLAG = "CTF{command_injection_flag}"

@app.route('/')
def index():
    return '''
        <h1>Echo Testing....</h1>
        <p>echo 명령어로 메세지를 출력 할 수 있습니다.</p><p>cat 명령어로 다른 파일을 열어볼 수 있습니다.</p>
<p>ls 명령어로 현재 파일의 목록을 볼 수 있습니다.</p>
 <form method="POST" action="/execute">
            echo <input type="text" name="command" placeholder="Enter your command" />
            <input type="submit" value="Execute" />
        </form>
        <!--Q. 그런데 명령어를 한 줄에 2개를 입력하고 싶을 땐 어떻게 해야하나요? 
    A. ; 
    Q. 대답하기 싫으신건가요?
    A. 그게; 아니라; ;는 명령어가 끝난 후 다음 명령어를 이어서 쓸 수 있게 하는 리눅스의 특수 기호입니다;
-->    '''

@app.route('/execute', methods=['POST'])
def execute():
    command = request.form.get('command')
    result = os.popen('echo '+str(command)).read()

    return render_template_string(f'''
        <h1>Result</h1>
        <pre>{result}</pre>
        <a href="/">Go back</a>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=25566)

