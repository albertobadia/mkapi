from threading import Thread
from time import time, sleep
from flask_restful import Resource
from temp_mk import TempMk
from parser import P

TEMP_MK_LIST = {}


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


class TempPing(Resource):
    def get(self):
        args = P.parser.parse_args()
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


class TempInterfaceTraffic(Resource):
    def get(self):
        args = P.parser.parse_args()
        host = args['host']
        username = args['username']
        password = args['password']
        port = args['port']
        interface = args.get("interface")

        temp_mk = TEMP_MK_LIST.get(host)
        if temp_mk:
            return temp_mk.get_interface_traffic(interface=interface)
        else:
            TEMP_MK_LIST[host] = TempMk(host=host, username=username, password=password, port=port)
            return TEMP_MK_LIST[host].get_interface_traffic(interface=interface)


class TempWireless(Resource):
    def get(self):
        args = P.parser.parse_args()
        host = args['host']
        username = args['username']
        password = args['password']
        port = args['port']

        temp_mk = TEMP_MK_LIST.get(host)
        if temp_mk:
            return temp_mk.get_wireless()
        else:
            TEMP_MK_LIST[host] = TempMk(host=host, username=username, password=password, port=port)
            return TEMP_MK_LIST[host].get_wireless()


class TempWirelessRegtable(Resource):
    def get(self):
        args = P.parser.parse_args()
        host = args['host']
        username = args['username']
        password = args['password']
        port = args['port']

        temp_mk = TEMP_MK_LIST.get(host)
        if temp_mk:
            return temp_mk.get_wireless_regtable()
        else:
            TEMP_MK_LIST[host] = TempMk(host=host, username=username, password=password, port=port)
            return TEMP_MK_LIST[host].get_wireless_regtable()
