import json
from pymongo import MongoClient
from bson import json_util
from datetime import datetime


MONGO_URI = 'mongodb://localhost:27017/'


class Mongo(object):

    connection = None

    def __init__(self, db, uri=None):
        if uri is None:
            uri = MONGO_URI
        if not Mongo.connection:
            Mongo.connection = MongoClient(uri)
        self.db = Mongo.connection[db]

    def query(self, col, find, skip, limit, cmd):
        q_json = None
        if find:
            q_json = json.loads(find)
        query_ = self.db[col].find(q_json)
        if skip:
            query_ = query_.skip(int(skip))
        if limit:
            query_ = query_.limit(int(limit))
        if cmd == 'count':
            if skip or limit:
                count = query_.count(with_limit_and_skip=True)
            else:
                count = query_.count(with_limit_and_skip=False)
            return json.dumps({'count': count})
        docs = [item for item in query_]

        return json.dumps(docs, sort_keys=True, indent=4,
                          default=json_util.default)

    def exists(self, item, collection, ident='identifier'):
        return (self.db[collection].find_one({ident: item[ident]}) is not None)

    def close(self):
        if Mongo.connection:
            Mongo.connection.disconnect()

    def import_file(self, collection_name, filename, identifier):
        collection = self.db[collection_name]
        collection.ensure_index(identifier, unique=True)

        with open(filename) as f:
            date_now = datetime.utcnow()
            for item_json in f:
                item = self.clean_item(json.loads(item_json))
                exists = self.exists(item={identifier: item[identifier]},
                                     collection=collection_name)
                if not exists:
                    item['date'] = date_now
                    collection.insert(item)
                else:
                    collection.update({identifier: item[identifier]},
                                      dict(item))

    '''
    Remove dot (.) and None values from keys
    '''
    @classmethod
    def clean_item(cls, item):
        new_item = {}
        for k, v in item.items():
            if k is not None:
                new_k = k.replace('.', '')
                if isinstance(v, dict):
                    new_item[new_k] = cls.clean_item(v)
                else:
                    new_item[new_k] = v
        return new_item
