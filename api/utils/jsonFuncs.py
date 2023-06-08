import json

def loadData(path):
    with open(path) as file:
        data = json.load(file)
        return data