# Repositório base para operações CRUD genéricas
from abc import ABC, abstractmethod
from typing import Optional, List, Any
from gem.utils.database import db


class BaseRepository(ABC):
    """Classe base para repositórios"""
    
    def __init__(self, model_class):
        self.model_class = model_class

    def create(self, **kwargs) -> Any:
        """Cria uma nova instância do modelo"""
        instance = self.model_class(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

    def get_by_id(self, id: int) -> Optional[Any]:
        """Busca uma instância por ID"""
        return self.model_class.query.get(id)

    def get_all(self) -> List[Any]:
        """Retorna todas as instâncias"""
        return self.model_class.query.all()

    def update(self, id: int, **kwargs) -> Optional[Any]:
        """Atualiza uma instância por ID"""
        instance = self.get_by_id(id)
        if instance:
            for key, value in kwargs.items():
                if hasattr(instance, key) and value is not None:
                    setattr(instance, key, value)
            db.session.commit()
        return instance

    def delete(self, id: int) -> bool:
        """Remove uma instância por ID"""
        instance = self.get_by_id(id)
        if instance:
            db.session.delete(instance)
            db.session.commit()
            return True
        return False

    def filter_by(self, **kwargs) -> List[Any]:
        """Filtra instâncias por critérios"""
        return self.model_class.query.filter_by(**kwargs).all()

    def exists(self, **kwargs) -> bool:
        """Verifica se existe uma instância com os critérios dados"""
        return self.model_class.query.filter_by(**kwargs).first() is not None