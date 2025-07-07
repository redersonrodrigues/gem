from abc import ABC, abstractmethod

class FormElementInterface(ABC):
    @abstractmethod
    def setName(self, name):
        pass

    @abstractmethod
    def getName(self):
        pass

    @abstractmethod
    def setValue(self, value):
        pass

    @abstractmethod
    def getValue(self):
        pass

    @abstractmethod
    def render(self):
        pass
