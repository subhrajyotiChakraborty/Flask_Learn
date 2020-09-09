from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    TABLE_NAME = "items"

    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="This field is required"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            return item.json()
        return {"message": f"Item with name {name} not found"}, 404

    def post(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            return {"message": f"Item with name {name} already exists"}, 400
        else:
            data = Item.parser.parse_args()
            new_item = ItemModel(name, data["price"])

            try:
                new_item.save_item_to_db()
            except:
                return {"message": "An error occurred while inserting the item."}, 500

            return new_item.json(), 201

    def delete(self, name):
        item = ItemModel.find_item_by_name(name)

        if item:
            item.delete_item()

        return {"message": "Item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_item_by_name(name)

        if item:
            item.price = data["price"]
        else:
            item = ItemModel(name, data["price"])

        try:
            item.save_item_to_db()
        except:
            return {"message": "An error occurred while inserting the item."}, 500

        return item.json()


class ItemList(Resource):
    def get(self):
        # return {"items": [item.json() for item in ItemModel.query.all()]}
        return {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}
