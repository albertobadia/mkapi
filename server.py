from librouteros import connect
from librouteros.login import plain

from flask import Flask
from flask_restful import Resource, Api

MK = connect(host='main.server', username='bctm', password='EPsystems7', port=65000, login_methods=plain)
path = MK.path("")

app = Flask(__name__)
api = Api(app)


class Ping(Resource):
    def get(self, address):
        try:
            result = tuple(path("ping", **{"address": address, "count": "1"}))[0]
            return result
        except Exception as e:
            print(e)
            exit()


api.add_resource(Ping, "/ping/<address>")
if __name__ == "__main__":
    app.run(debug=True)
