from flask_restful import Resource
from mk import MK


class Ping(Resource):
    def get(self, address):
        try:
            path = MK.path("")
            result = tuple(path("ping", **{"address": address, "count": "1"}))[0]
            return result
        except Exception as e:
            print(e)
            exit()