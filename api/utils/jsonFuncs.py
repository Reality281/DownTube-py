import json

def loadData(path):
    path = f'../{str(path).strip('/')}'
    try:
        with open(path) as file:
            data = json.load(file)
            return data
    except Exception as e:
        return f'An error occured while getting the data from "{path}"'