import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()


create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text NOT NULL UNIQUE, password text NOT NULL, description text,tags text,coursesTakingId integrer,FOREIGN KEY (coursesTakingId) REFERENCES courses (id))"
cursor.execute(create_table)
create_table = "CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY, name text NOT  NULL UNIQUE,content not null, adminId integrer NOT NULL, description text,tags text,image,FOREIGN KEY (adminId) REFERENCES users (id) )"
cursor.execute(create_table)



connection.commit()

connection.close()