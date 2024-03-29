def loadData(path):
    import json
    try:
        with open(f'api/{path}') as file:
            data = json.load(file)
            return data
    except Exception as e:
        return f'An error occured while getting the data from "{path}", {e}'