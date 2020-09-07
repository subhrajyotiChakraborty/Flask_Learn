import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

user = (1, "Jack", "1234")
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

users = [
    (2, "Mike", "1234"),
    (3, "Linda", "1234")
]
cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
user_list = cursor.execute(select_query)
for user in user_list:
    print(user)
    print(user[1])

connection.commit()

connection.close()
