import falcon
import json
import pymongo
import waitress

class HelloResource(object):

    def on_get(self, req, resp):
        msg = {
            "message": "Welcome to the Falcon"
        }
        resp.body = json.dumps(msg)

app = falcon.API()
app.add_route("/", HelloResource())

from waitress import serve
serve(app, listen='*:8080')