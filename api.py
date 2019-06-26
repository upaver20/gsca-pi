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
        resp.body = json.dumps(msg, cls=DateTimeSupportJSONEncoder, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


class UserData(object):
    def on_get(self, req, resp, id):
        client = pymongo.MongoClient()
        db = client['r6status']
        old = db['old']
        id2uid = db['id2uid']

        # prm = req.params()
        # print(prm['count'])

        uid = list(id2uid.find({'id': id}, {'_id': 0})
                   .sort('date', pymongo.DESCENDING))[0]["uid"]
        user_data = list(old.find({'uid': uid}, {'_id': 0}).sort('date', pymongo.DESCENDING))

        count = req.get_param_as_int('count')

        if count == None:
            count = 0
        if count > len(user_data)  or count == 0:
            count = len(user_data)

        msg = user_data[0:count]

        if msg:
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(msg, cls=DateTimeSupportJSONEncoder, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

        else:
            errmsg = {
                "message": "ID was not valid."
            }
            resp.status = falcon.HTTP_404
            resp.body = json.dumps(errmsg, cls=DateTimeSupportJSONEncoder, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

    def on_post(self, req, resp, id):
        client = pymongo.MongoClient()
        db = client['r6status']
        dead_iddb = db['dead_id']
        date = datetime.utcnow()

        dead_id.update({"id": id}, { '$set': {"date": date}, '$inc': {"deathcount": 1}}, upsert=True)

        msg = {
            "message": "success to add DataBase"
        }
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(msg, cls=DateTimeSupportJSONEncoder, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

    class CORSMiddleware:
        def process_request(self, req, resp):
            resp.set_header('Access-Control-Allow-Origin', '*')


app = falcon.API(middleware=[CORSMiddleware()])
app.add_route("/hello", HelloResource())
app.add_route("/userlist", UserList())
app.add_route("/userdata/{id}", UserData())

serve(app, listen='*:27802')
