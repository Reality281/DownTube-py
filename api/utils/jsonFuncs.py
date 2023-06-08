def loadData(path):
    import json
    try:
        newPath = str(path).strip('./')
    except:
        newPath = str(path).strip('/')
    finally:
        path = f'../{newPath}'
    try:
        with open(path) as file:
            data = json.load(file)
            return data
    except Exception as e:
        return f'An error occured while getting the data from "{path}", {e}'