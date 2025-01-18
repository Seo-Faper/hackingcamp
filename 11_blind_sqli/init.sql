-- users 테이블 생성
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

-- 플래그 테이블 생성
CREATE TABLE IF NOT EXISTS flags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flag TEXT NOT NULL
);

-- users 테이블 초기 데이터 삽입
INSERT INTO users (username, password) VALUES ('admin', 'adminpass');
INSERT INTO users (username, password) VALUES ('user', 'userpass');

-- flags 테이블 초기 데이터 삽입 (플래그 추가)
INSERT INTO flags (flag) VALUES ('cbcamp{BLIND_SQL_INJECTION_FLAG}');
