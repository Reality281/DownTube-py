def loadData(path):
    import json
    path = str(path).replace('../', '') if str(path).startswith('../') else str(path).replace('./', '') if str(path).startswith('./') else str(path)
    path = f'api/{path}'
    try:
        with open(path) as file:
            data = json.load(file)
            return data
    except Exception as e:
        return f'An error occured while getting the data from "{path}", {e}'