from werkzeug.security import safe_str_cmp
from user import User

users = [
    User(1, "Jack", "1234")
]

username_mapping = {u.username: u for u in users}

userid_mapping = {u.id: u for u in users}


def authenticate(username, password):
    user = username_mapping.get(username, None)
    print(user)
    if user and user.password == str(password):
        return user


def identity(payload):
    user_id = payload["identity"]
    return userid_mapping.get(user_id, None)
