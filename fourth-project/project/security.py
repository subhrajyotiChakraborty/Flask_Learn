from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_usersname(username)
    print(user)
    if user and user.password == str(password):
        return user


def identity(payload):
    user_id = payload["identity"]
    return UserModel.find_by_userid(user_id)
