from librouteros.query import Key
from flask_restful import Resource
from mk import MK
from parser import P

key_name = Key('name')
key_rate = Key('rate')


class Ping(Resource):
    def get(self, address):
        try:
            path = MK.path("")
            return tuple(path("ping", **{"address": address, "count": "1"}))[0]
        except Exception as e:
            print(e)
            exit()


class ArpPing(Resource):
    def get(self):
        try:
            args = P.parser.parse_args()
            address = args.get("address")
            interface = args.get("interface")
            data = {"address": address, "count": "1", "arp-ping": "yes", "interface": interface}
            path = MK.path("")
            return tuple(path("ping", **data))[0]
        except Exception as e:
            print(e)
            exit()


class QueueTraffic(Resource):
    def get(self, name):
        try:
            result = False

            while not result:
                for row in MK.path("/queue/simple").select(key_rate).where(key_name == name):
                    if row:
                        result = row

            return result
        except Exception as e:
            print(e)
            exit()


class InterfaceTraffic(Resource):
    def get(self):
        try:
            args = P.parser.parse_args()
            interface = args.get("interface")

            path_interfaces = MK.path("interface")
            traffic = tuple(path_interfaces('monitor-traffic', **{'duration': 1, 'interface': interface}))
            return traffic[0]
        except Exception as e:
            print(e)
            exit()
