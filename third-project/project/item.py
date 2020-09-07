import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    TABLE_NAME = "items"

    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="This field is required"
                        )

    @classmethod
    def find_item_by_name(cls, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {"item": {"name": row[0], "price": row[1]}}

    @classmethod
    def insert_item(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item["name"], item["price"]))

        connection.commit()
        connection.close()

    @classmethod
    def update_item(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item["price"], item["name"]))

        connection.commit()
        connection.close()

    @jwt_required()
    def get(self, name):
        item = self.find_item_by_name(name)
        if item:
            return item
        return {"message": f"Item with name {name} not found"}, 404

    def post(self, name):
        item = self.find_item_by_name(name)
        if item:
            return {"message": f"Item with name {name} already exists"}, 400
        else:
            data = Item.parser.parse_args()
            new_item = {"name": name, "price": data["price"]}

            try:
                self.insert_item(new_item)
            except:
                return {"message": "An error occurred while inserting the item."}, 500

            return new_item, 201

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

        item = self.find_item_by_name(name)
        updated_item = {"name": name, "price": data["price"]}

        if item:
            try:
                self.update_item(updated_item)
            except:
                return {"message": "An error occurred while updating the item."}, 500
        else:
            item = {"name": name, "price": data["price"]}
            try:
                self.insert_item(updated_item)
            except:
                return {"message": "An error occurred while inserting the item."}, 500

        return updated_item


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