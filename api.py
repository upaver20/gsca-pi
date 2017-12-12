import falcon
import json
import pymongo
from waitress import serve
from datetime import datetime

class DateTimeSupportJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super(DateTimeSupportJSONEncoder, self).default(o)

class HelloResource(object):

    def on_get(self, req, resp):
        msg = {
            "message": "Welcome to the Falcon"
        }
        resp.body = json.dumps(msg)

class UserList(object):
    def on_get(self, req, resp):
        client = pymongo.MongoClient()
        db = client['r6status']
        recent = db['recent']
        user_list = recent.find({}, {'_id': 0,'id':1,'date':1})
        msg = []
        for user in user_list:
            msg.append(user)

        resp.body = json.dumps(msg, cls=DateTimeSupportJSONEncoder )
        

app = falcon.API()
app.add_route("/hello", HelloResource())
app.add_route("/userlist", UserList())

serve(app, listen='*:8080')