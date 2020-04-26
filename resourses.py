from librouteros.query import Key
from flask_restful import Resource
from mk import MK

key_name = Key('name')
key_rate = Key('rate')


class Ping(Resource):
    def get(self, address):
        try:
            path = MK.path("")
            result = tuple(path("ping", **{"address": address, "count": "1"}))[0]
            return result
        except Exception as e:
            print(e)
            exit()


class QueueTraffic(Resource):
    def get(self, name):
        try:
            return MK.path("/queue/simple").select(key_rate).where(key_name == name)[0]
        except Exception as e:
            print(e)
            exit()
