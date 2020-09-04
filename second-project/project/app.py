from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "secret"
api = Api(app)

items = []

jwt = JWT(app, authenticate, identity)


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="This field is required"
                        )

    @jwt_required()
    def get(self, name):
        item = next(
            filter(lambda x: x["name"].lower() == name.lower(), items), None)
        if item:
            return item
        else:
            return {"message": f"Item with {name} not found"}, 404

    def post(self, name):
        if next(filter(lambda x: x["name"].lower() == name.lower(), items), None) is not None:
            return {"message": f"Item with name {name} already exists"}, 400
        else:
            data = Item.parser.parse_args()
            new_item = {"name": name, "price": data["price"]}
            items.append(new_item)
            return new_item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message": "Item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x["name"] == name, items), None)
        if item is None:
            item = {"name": name, "price": data["price"]}
            items.append(item)
        else:
            item.update(data)

        return item


class ItemList(Resource):
    def get(self):
        return {"items": items}


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")

app.run(port=5000, debug=True)
