import json
from pymongo import MongoClient


def load_to_mongodb(json_file, collection_name):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    client = MongoClient('mongodb+srv://galapetrovna77:1234567vocem@goithw.q1427.mongodb.net/')
    db = client['hwdb']
    collection = db[collection_name]

    if isinstance(data, list):
        collection.insert_many(data)
    elif isinstance(data, dict):
        collection.insert_one(data)


if __name__ == "__main__":
    load_to_mongodb('quotes.json', 'quotes')
    load_to_mongodb('authors.json', 'authors')