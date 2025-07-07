from abc import ABC, abstractmethod

class ActionInterface(ABC):
    @abstractmethod
    def set_parameter(self, param, value):
        pass

    @abstractmethod
    def serialize(self):
        pass