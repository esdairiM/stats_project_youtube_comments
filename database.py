import pymongo as mongo
import logging



class database:
    toknized_prefix = 'tokenized'
    def __init__(self, logger=None, dbname, port=27017, hostname="localhost", default_collection=""):
        self.logger = logger or logging.getLogger(__name__)
        self._client=mongo.MongoClient(__hostname__,__port__)
        self._db=self.__client[__bdname__]

    def create_collection(self, collection_name, have_tokenized_version=False):
        pymongo.collection.Collection(self._db,collection_name,create=True)
        if have_tokenized_version:
            pymongo.collection.Collection(self._db, 'tokenized'+collection_name, create=True)

    def create_text_index(self, collection_name, indexed_field, index_type, have_tokenized_version=False, default_lang='english'):
        self._db[collection_name].create_index([(indexed_field, pymongo.TEXT)], default_language=default_lang)
        if have_tokenized_version:
            self._db[toknized_prefix+collection_name].create_index(
                [(indexed_field, pymongo.TEXT)], default_language=default_lang)
        
    def insert_one(self, item, collection_name=self.__collection_name):
        return self._db[collection_name].insert_one(item)

    def insert_many(self, items, collection_name=self.__collection_name):
        return self._db[collection_name].insert_many(items)

    def find_by_videoId(self, **kargs, collection_name=self.__collection_name):
        return self._db[collection_name]find({'videoId': videoId})

