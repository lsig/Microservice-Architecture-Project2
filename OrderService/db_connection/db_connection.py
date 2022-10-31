from abc import ABC, abstractmethod

#TODO
class DbConnection(ABC):
    @abstractmethod
    def execute():
        pass

    @abstractmethod
    def commit():
        pass

    
    @abstractmethod
    def run_migrations():
        #TODO implement here
        pass