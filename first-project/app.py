from flask import Flask, jsonify, request, render_template
from markupsafe import escape

app = Flask(__name__)
stores = [
    {
        "name": "Store One",
        "items": [
            {
                "name": "Item One in store one",
                "price": 14.99
            }
        ]
    }
]


@app.route("/hello/")
def hello():
    return render_template("hello.html")


@app.route("/store", methods=["POST"])
def create_store():
    request_data = request.get_json()
    new_store = {
        "name": request_data["name"],
        "items": []
    }
    stores.append(new_store)
    return jsonify(new_store)


@app.route("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store["name"].lower() == name.lower():
            return jsonify({"store": store})
    return jsonify({"message": f"Store with {escape(name)} not found"})


@app.route("/store")
def get_stores():
    return jsonify({"stores": stores})


@app.route("/store/<string:name>/item", methods=["POST"])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"].lower() == name.lower():
            new_item = {
                "name": request_data["name"],
                "price": request_data["price"]
            }
            store["items"].append(new_item)
            return jsonify({"items": store["items"]})
    return jsonify({"message": f"Store with {escape(name)} not found"})


@app.route("/store/<string:name>/item")
def get_item_in_store(name):
    print(name.lower())
    for store in stores:
        if store["name"].lower() == name.lower():
            return jsonify({"items": store["items"]})
    return jsonify({"message": f"Store with {escape(name)} not found"})


app.run(port=5000)
