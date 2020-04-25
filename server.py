from time import sleep, time

from librouteros import connect
from librouteros.login import plain

from flask import Flask
from flask_restful import Resource, Api, reqparse

from threading import Thread

MK = connect(host='main.server', username='bctm', password='EPsystems7', port=65000, login_methods=plain)
path = MK.path("")

app = Flask(__name__)
api = Api(app)

TEMP_MK_LIST = {}

PARSER = reqparse.RequestParser()
PARSER.add_argument('host', type=str)
PARSER.add_argument('username', type=str)
PARSER.add_argument('password', type=str)
PARSER.add_argument('port', type=int)
PARSER.add_argument('address', type=str)


class TempCleaner(Thread):
    def run(self):
        while True:
            now = time()

            try:
                for mk in TEMP_MK_LIST:
                    last_activity = TEMP_MK_LIST[mk].last_activity
                    seconds = int(now - last_activity)
                    if seconds > 60:
                        print("Closing connection on: {0}".format(mk))
                        TEMP_MK_LIST[mk].close()
                        TEMP_MK_LIST.pop(mk)
            except Exception as e:
                print(e)

            sleep(30)


class TempMk:
    def __init__(self, host, username, password, port, login_methods=plain):
        self.is_connected = False
        self.error = "Error message"
        self.last_activity = None
        self.api = None
        self.path = None

        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.login_methods = login_methods

        self.connect()

    def close(self):
        self.api.close()

    def connect(self):
        try:
            self.api = connect(
                host=self.host, username=self.username, password=self.password, port=self.port,
                login_methods=self.login_methods
            )
            self.path = self.api.path("")
            self.last_activity = time()
            self.is_connected = True
        except Exception as e:
            self.error = e

    def ping(self, address):
        if self.is_connected:
            self.last_activity = time()
            return tuple(self.path("ping", **{"address": address, "count": "1"}))
        else:
            return {"error": self.error}


class Ping(Resource):
    def get(self, address):
        try:
            result = tuple(path("ping", **{"address": address, "count": "1"}))[0]
            return result
        except Exception as e:
            print(e)
            exit()


class TempPing(Resource):
    def get(self):
        args = PARSER.parse_args()
        host = args['host']
        username = args['username']
        password = args['password']
        port = args['port']
        address = args['address']

        temp_mk = TEMP_MK_LIST.get(host)
        if temp_mk:
            return temp_mk.ping(address=address)
        else:
            TEMP_MK_LIST[host] = TempMk(host=host, username=username, password=password, port=port)
            return TEMP_MK_LIST[host].ping(address=address)


cleaner = TempCleaner()
cleaner.start()

api.add_resource(Ping, "/ping/<address>")
api.add_resource(TempPing, "/temp/ping")
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
