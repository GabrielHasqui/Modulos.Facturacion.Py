from storage.json_storage import JsonFile
from storage.file_manager import data_path


class FacturaService:
    def __init__(self):
        self.storage = JsonFile(data_path("facturas.json"))

    def listar(self):
        return self.storage.read()
