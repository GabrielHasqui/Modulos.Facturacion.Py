import json


class JsonFile:
    def __init__(self, filename):
        self.filename = filename

    def save(self, data):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def read(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        return data

    def find(self, atributo, buscado):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                datas = json.load(file)
                data = [item for item in datas if item.get(atributo) == buscado]
        except FileNotFoundError:
            data = []
        return data
