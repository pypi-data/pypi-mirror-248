import pydantic
import re


class DBModelMetaClass(pydantic.main._model_construction.ModelMetaclass):
    def __new__(mcs, name, bases, dct):
        cls = super().__new__(mcs, name, bases, dct)
        cls.model_config['arbitrary_types_allowed'] = True   # but, be careful if you use them!
        cls.__db_name__ = cls.model_config.get(
            'table_name',
            re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower())

        cls._db = None

        for name, field in cls.__fields__.items():
            setattr(cls, name, field)
        return cls

    @property
    def __db__(cls):
        return cls.handle_db_property(cls)

    @staticmethod
    def handle_db_property(cls):
        """Return the database client with model collection"""
        pass


class BaseDataModel(pydantic.BaseModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.key = self.key or None

    @classmethod
    def db(cls):
        return cls.__db__

    @classmethod
    def get(cls, key):
        pass

    @classmethod
    def get_all(cls):
        pass

    @classmethod
    def delete_key(cls, key):
        pass

    @classmethod
    def query(cls, statement):
        pass

    def update(self, update_data: dict):
        pass

    def save(self):
        pass

    def get_attribute_value(self, index=1):
        d = self.__dict__
        return list(d.values())[index]
