from abc import ABC, abstractmethod


class IPyMongoDb(ABC):

    # return { "name": "x", "age": "y"..... } = dictionary
    @abstractmethod
    def to_dict(self):
        pass
    
    @staticmethod
    @abstractmethod # a static function, returns an instance of the class.
    def from_dict(self):
        pass
    
    #     def to_dict(self):
    #     return { "id": self.id, "name": self.name }
    
    # def from_dict(dictionary):
    #     return User(dictionary.get("id"), dictionary.get("name"))