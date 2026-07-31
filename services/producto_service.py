from storage.json_storage import JsonFile
from storage.file_manager import data_path


class ProductoService:
    def __init__(self):
        self.storage = JsonFile(data_path("productos.json"))

    def listar(self):
        return self.storage.read()
