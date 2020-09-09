import sqlite3
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
                new_item.insert_item()
            except:
                return {"message": "An error occurred while inserting the item."}, 500

            return new_item.json(), 201

    def delete(self, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {"message": "Item deleted"}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_item_by_name(name)
        updated_item = ItemModel(name, data["price"])

        if item:
            try:
                updated_item.update_item()
            except:
                return {"message": "An error occurred while updating the item."}, 500
        else:
            try:
                updated_item.insert_item()
            except:
                return {"message": "An error occurred while inserting the item."}, 500

        return updated_item.json()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)

        items = []
        for row in result:
            items.append({"name": row[0], "price": row[1]})

        connection.close()

        return {"items": items}
