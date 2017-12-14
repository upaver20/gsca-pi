#!/home/upaver20/.anyenv/envs/pyenv/versions/falcon/bin/python
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

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(msg)


class UserList(object):
    def on_get(self, req, resp):
        client = pymongo.MongoClient()
        db = client['r6status']
        recent = db['recent']
        msg = list(recent.find({}, {'_id': 0, 'id': 1, 'date': 1}))

        resp.status = falcon.HTTP_200
        resp.body = json.dumps(msg, cls=DateTimeSupportJSONEncoder)


class UserData(object):
    def on_get(self, req, resp,id):
        client = pymongo.MongoClient()
        db = client['r6status']
        old = db['old']

        user_data = list(old.find({'id': id}, {'_id': 0})
                   .sort('date', pymongo.DESCENDING)) 

        count = req.get_param_as_int('count')

        if count == None:
            count = 0
        if count > len(user_data):
            count = len(user_data)

        msg = user_data[0:count]

        if msg:
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(msg, cls=DateTimeSupportJSONEncoder)

        else:
            errmsg = {
                "message": "ID was not valid."
            }
            resp.status = falcon.HTTP_404
            resp.body = json.dumps(errmsg, cls=DateTimeSupportJSONEncoder)

    def on_post(self, req, resp, id):
        client = pymongo.MongoClient()
        db = client['r6status']
        userdb = db['user']
        date = datetime.utcnow()

        userdb.update({"id": id}, {'$set': {"deathcount": 0}}, upsert=True)
        userdb.update({"id": id}, {'$set': {"date": date}}, upsert=True)
        msg = {
            "message": "success to add DataBase"
        }
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(msg, cls=DateTimeSupportJSONEncoder)


app = falcon.API()
app.add_route("/hello", HelloResource())
app.add_route("/userlist", UserList())
app.add_route("/userdata/{id}", UserData())

serve(app, listen='*:27802')
