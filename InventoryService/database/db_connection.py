


from abc import ABC, abstractmethod


class DbConnection(ABC):
    
    @abstractmethod
    def execute():
        pass

    @abstractmethod
    def commit():
        pass