CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

INSERT INTO users (username, password) VALUES ('admin', 'cbcamp{SQL_INJec7iOn_CHall}');
INSERT INTO users (username, password) VALUES ('user', 'userpass');

