import logging

import pymongo as mongo


class Database:

    def __init__(self, configuration, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self._client = mongo.MongoClient(configuration['hostname'], configuration['port'])
        self._db = self._client[configuration['bdname']]

    def create_collection(self, collection_name, have_tokenized_version=False):
        try:
            mongo.collection.Collection(self._db, collection_name, create=True)
            if have_tokenized_version:
                mongo.collection.Collection(self._db, 'tokenized' + collection_name, create=True)
        except mongo.errors.PyMongoError:
            raise Exception('collection already exist')

    def create_text_index(self, collection_name, indexed_field, have_tokenized_version=False, default_lang='english'):
        try:
            self._db[collection_name].create_index([(indexed_field, mongo.TEXT)], default_language=default_lang)
            if have_tokenized_version:
                self._db[self.toknized_prefix + collection_name].create_index(
                    [(indexed_field, mongo.TEXT)],
                    default_language=default_lang
                )
        except mongo.errors.PyMongoError:
            raise Exception('failed at creating index')

    def insert_preprocessed_data(self, collection_name, items):
        res = self._db['tokenized' + collection_name].insert_many(items)
        return res

    def insert_data(self, collection_name, items):
        return self._db[collection_name].insert_many(items)

    def find_by_video_id(self, collection_name, video_id):
        return self._db[collection_name].find({'videoId': video_id})

    def find_by_expression(self, collection_name, text):
        return self._db[collection_name].find({'$text': {'$search': text}})
