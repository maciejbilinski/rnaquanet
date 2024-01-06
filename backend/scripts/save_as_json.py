from flask import json


# saves given data as json
def save_as_json(data: any, path: str):
    with open(path, 'w+') as file:
        json.dump(data, file, indent=2)