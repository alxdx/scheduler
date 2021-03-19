import json, bson

class MongoJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bson.ObjectId):
            return str(obj)

        return json.JSONEncoder.default(self, obj)
