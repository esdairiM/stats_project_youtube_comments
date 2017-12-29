import logging

import pymongo as mongo


class Database:

    def __init__(self, configuration, logger=None):
        """

        :param configuration:
        :param logger:
        """
        try:
            self.logger = logger or logging.getLogger(__name__)
            self._client = mongo.MongoClient(configuration['hostname'], configuration['port'])
            self._db = self._client[configuration['bdname']]
        except mongo.errors.PyMongoError:
            raise Exception('Error initializing database')

    def create_store(self, collection_name, have_tokenized_version=False):
        """
        this method create a collection in mongodb database
        :param collection_name: the collection name
        :param have_tokenized_version: default to false, true will create a second collection
        with prefix "token_"
        """
        try:
            mongo.collection.Collection(self._db, collection_name, create=True)
            if have_tokenized_version:
                mongo.collection.Collection(self._db, 'token_' + collection_name, create=True)
        except mongo.errors.PyMongoError:
            raise Exception('collection already exist')

    def create_text_index(self, collection_name, indexed_field, have_tokenized_version=False, default_lang='english'):
        """

        :param collection_name:
        :param indexed_field: field to be indexed
        :param have_tokenized_version: does the collection have a tokenized version to be indexed, default to false
        :param default_lang: default language for indexing english
        """
        try:
            self._db[collection_name].create_index([
                (indexed_field, mongo.TEXT),
                ({'language_override': 'lang'})
            ])
            if have_tokenized_version:
                self._db[self.toknized_prefix + collection_name].create_index(
                    [(indexed_field, mongo.TEXT)],
                    default_language=default_lang
                )
        except mongo.errors.PyMongoError:
            raise Exception('Index already exist')

    def insert_preprocessed_data(self, collection_name, items):
        """
        :param collection_name:
        :param items:
        :return :generated for keys of inserted elements if success else false
        """
        try:
            return self._db['token_' + collection_name].insert_many(items)
        except mongo.errors.PyMongoError:
            raise Exception('failed to insert processed data')
        return False

    def insert(self, collection_name, items):
        """
        :param collection_name:
        :param items:
        :return :generated for keys of inserted elements if success else false
        """
        try:
            return self._db[collection_name].insert_many(items)
        except mongo.errors.PyMongoError:
            raise Exception('failed to insert data')

    def find_by_video_id(self, collection_name, video_id,kvargs={}):
        """

        :param collection_name:
        :param video_id:
        :param kvargs: {"key":val,...}possible key="comment","videoId","created_at","author", "lang", "likes","_id"
        possible val:1 to fetch,0 to ignore
        :return:
        """
        try:
            return self._db[collection_name].find({'videoId': video_id}, kvargs)
        except mongo.errors.PyMongoError:
            raise Exception('failed to find video by id')

    def find_by_expression(self, collection_name, query):
        """
        execute find query
        :param collection_name:
        :param query:
        :return:query results
        {'$text': {'$search': text}}
        """
        try:
            return self._db[collection_name].find(query)
        except mongo.errors.PyMongoError:
            raise Exception('failed to execute find request')
