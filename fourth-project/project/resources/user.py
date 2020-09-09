from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True,
                        help="This field is required")
    parser.add_argument("password", type=str, required=True,
                        help="This field is required")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_usersname(data["username"]):
            return {"message": f"User with {data['username']} already exists"}, 400

        try:
            # user = UserModel(data["username"], data["password"]) we can use **data
            user = UserModel(**data)
            user.save_user_to_db()
        except:
            return {"message": "An error occurred while saveing the user."}, 500

        return {"message": "User created"}, 201
