def loadData(path):
    import json, os
    path = os.path.join(os.getcwd(), f'../{path}')
    try:
        with open(path) as file:
            data = json.load(file)
            return data
    except Exception as e:
        return f'An error occured while getting the data from "{path}", {e}'