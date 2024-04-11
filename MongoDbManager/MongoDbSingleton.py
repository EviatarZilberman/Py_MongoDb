from pymongo import MongoClient
from bson.objectid import ObjectId


class MongoDbSingleton:
    __m_client = None
    __m_db = None
    __m_collection = None
    m_instance = None

    def __new__(cls, db, collection, domain = "localhost", port = 27017, *args, **kwargs):
        if cls.m_instance is None:
         cls.m_instance = super().__new__(cls, *args, **kwargs)
         cls.__m_client = MongoClient(domain, port)
         cls.m_instance.__m_db = cls.__m_client[db]
         cls.m_instance.__m_collection = cls.m_instance.__m_db[collection]
        return cls.m_instance

    @classmethod
    def re_init_instance(self, reset_client = None):
        if reset_client:
            self.__m_client = None
        self.__m_db = None
        self.__m_collection = None
        self.m_instance = None
        pass

    def insert(self, inserted):
        self.__m_collection.insert_one(inserted.to_dict())
        pass

    def find_all(self):
        return self.__m_collection.find()

    def find_by_id(self, id):
        return self.__m_collection.find_one({"_id": ObjectId(id)})

    def find_by_key_value(self, key, value):
        result = list(self.__m_collection.find({key: value}))
        return result
    #
    # def update_member(self, id, key, newValue):
    #     is_instance = MongoDbSingleton.is_object(newValue)
    #     if not is_instance:
    #         dict_new_value = newValue.to_dict()
    #     else:
    #         dict_new_value = newValue
    #     self.__m_collection.update_one({"_id": ObjectId(id)}, {"$set": {key: dict_new_value}})

    def update_member(self, id, key, new_value):
        res = None
        try:
            res = hasattr(new_value, "to_dict") and callable(new_value.to_dict)
        except Exception as e:
            print(e)
        if res:
            dict_new_value = new_value.to_dict()
        else:
            dict_new_value = new_value
        self.__m_collection.update_one({"_id": ObjectId(id)}, {"$set": {key: dict_new_value}})

    def delete_by_id(self, id):
        return self.__m_collection.delete_one({"_id": ObjectId(id)})

    def replace_member(self, new_instance):
        self.__m_collection.replace_one({ "_id": new_instance.m_internal_id }, new_instance.to_dict())
        pass

    def find_one_by_key_value(self, key, value):
        result = self.__m_collection.find_one({key: value})
        return result

    @staticmethod
    def is_object(arg):
        return isinstance(arg, str)

    @staticmethod
    def reinitialize(db=None, collection=None, domain='localhost', port=27017):
        MongoDbSingleton.__m_db = None
        MongoDbSingleton.__m_collection = None
        MongoDbSingleton.__m_client = None
        MongoDbSingleton.m_instance = None

        if db is not None and collection is not None:
            MongoDbSingleton.__m_client = MongoClient(domain, port)
            MongoDbSingleton.m_instance = MongoDbSingleton()
            MongoDbSingleton.m_instance.__m_db = MongoDbSingleton.__m_client[db]
            MongoDbSingleton.m_instance.__m_collection = MongoDbSingleton.m_instance.__m_db[collection]