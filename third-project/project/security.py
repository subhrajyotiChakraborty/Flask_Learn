from werkzeug.security import safe_str_cmp
from user import User


def authenticate(username, password):
    user = User.find_by_usersname(username)
    print(user)
    if user and user.password == str(password):
        return user


def identity(payload):
    user_id = payload["identity"]
    return User.find_by_userid(user_id)
