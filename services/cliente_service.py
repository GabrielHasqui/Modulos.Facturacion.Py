from abc import ABC, abstractmethod
from storage.json_storage import JsonFile
from storage.file_manager import data_path

class ICrud(ABC):
 
    @abstractmethod    
    def create():
        pass
    @abstractmethod   
    def update():
        pass
    @abstractmethod 
    def delete():
        pass
    @abstractmethod 
    def consult():
        pass


class ClienteService:
    def __init__(self):
        self.storage = JsonFile(data_path("clientes.json"))

    def listar(self):
        return self.storage.read()
