import falcon
import json
import pymongo
from waitress import serve
from datetime import datetime
def validate(req, resp, resource, params):
    try:
        params['id'] = int(params['id'])
    except ValueError:
        raise falcon.HTTPBadRequest('Invalid ID','ID was not valid.')

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
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(msg)

class UserList(object):
    def on_get(self, req, resp):
        client = pymongo.MongoClient()
        db = client['r6status']
        recent = db['recent']
        msg = []

        for user in recent.find({}, {'_id': 0,'id':1,'date':1}):
            msg.append(user)

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(msg, cls=DateTimeSupportJSONEncoder )

class UserData(object):
    def on_get(self, req, resp, id):
        client = pymongo.MongoClient()
        db = client['r6status']
        old = db['old']

        msg = []
        user_data = old.find({'id':id},{'_id':0}).sort('date', pymongo.DESCENDING)
        for data in user_data:
            msg.append(data)

        resp.body = json.dumps(msg, cls=DateTimeSupportJSONEncoder )

app = falcon.API()
app.add_route("/hello", HelloResource())
app.add_route("/userlist", UserList())
app.add_route("/userdata/{id}", UserData())

serve(app, listen='*:8080')