from librouteros.query import Key
from flask_restful import Resource
from mk import MK

name = Key('name')
rate = Key('rate')


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
    def get(self, _name):
        try:
            return MK.path("/queue/simple").select(rate).where(name == _name)

        except Exception as e:
            print(e)
            exit()
