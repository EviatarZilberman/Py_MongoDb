from pymongo import MongoClient, errors
from bson.objectid import ObjectId


class MongoDbSingleton:
    _client = None
    _db = None
    _collection = None
    _instance = None

    def __new__(cls, db, collection, domain = "localhost", port = 27017, *args, **kwargs):
        try:
            if cls._instance is None:
                cls._instance = super().__new__(cls, *args, **kwargs)
                cls._client = MongoClient(domain, port)
                cls._instance._db = cls._client[db]
                cls._instance._collection = cls._instance._db[collection]
                return cls._instance
        except Exception as e:
            print(str(e))
            pass

    @classmethod
    def re_init_instance(cls, reset_client = None):
        if reset_client:
            cls._client = None
        cls._db = None
        cls._collection = None
        cls._instance = None
        pass

    def insert(self, inserted):
        self._collection.insert_one(inserted.to_dict())

    def find_all(self):
        return self._collection.find()

    def find_by_id(self, item_id: str):
        return self._collection.find_one({"_id": ObjectId(item_id)})

    def find_by_key_value(self, key, value):
        try:
            result = list(self._collection.find({key: value}))
            return result
        except Exception as e:
            print(str(e))
            return None

    def update_member(self, item_id, key, new_value):
        res = None
        try:
            res = hasattr(new_value, "to_dict") and callable(new_value.to_dict)
        except Exception as e:
            print(e)
        if res:
            dict_new_value = new_value.to_dict()
        else:
            dict_new_value = new_value
        self._collection.update_one({"_id": ObjectId(item_id)}, {"$set": {key: dict_new_value}})

    def delete_by_id(self, item_id):
        try:
            result = self._collection.delete_one({"_id": ObjectId(item_id)})
            if result.deleted_count == 1:
                print("Document deleted successfully.")
            else:
                print("Document with specified ID not found.")
        except errors.PyMongoError as e:
            print(f"An error occurred while deleting document: {e}")

    # def delete_by_id(self, id):
    #     self.__m_collection.delete_one({"_id": ObjectId(id)})
    #     pass

    def replace_member(self, new_instance):
        self._collection.replace_one({ "_id": new_instance.internal_id }, new_instance.to_dict())

    def find_one_by_key_value(self, key, value):
        try:
            result = self._collection.find_one({key: value})
            return result
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def reinitialize(db=None, collection=None, domain='localhost', port=27017):
        MongoDbSingleton._db = None
        MongoDbSingleton._collection = None
        MongoDbSingleton._client = None
        MongoDbSingleton._instance = None

        if db is not None and collection is not None:
            MongoDbSingleton._client = MongoClient(domain, port)
            MongoDbSingleton._instance = MongoDbSingleton()
            MongoDbSingleton._instance._db = MongoDbSingleton._client[db]
            MongoDbSingleton._instance._collection = MongoDbSingleton._instance._db[collection]