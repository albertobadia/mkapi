from time import time
from librouteros import connect
from librouteros.login import plain


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
                login_methods=plain
            )
            self.path = self.api.path("")
            self.last_activity = time()
            self.is_connected = True
        except Exception as e:
            self.error = e

    def ping(self, address):
        if self.is_connected:
            self.last_activity = time()
            return tuple(self.path("ping", **{"address": address, "count": "1"}))[0]
        else:
            return {"error": self.error}

    def get_interface_traffic(self, interface=False):
        if self.is_connected:
            if interface:
                path_interfaces = self.api.path("interface")
                traffic = tuple(path_interfaces('monitor-traffic', **{'duration': 1, 'interface': interface}))
                return traffic[0]
            else:
                return {"error": "Not obtain interface name"}
        else:
            return {"error": self.error}

    def get_wireless(self):
        if self.is_connected:
            path_wireless = self.api.path("interface", "wireless")
            wireless = tuple(path_wireless)
            return wireless[0]
        else:
            return {"error": self.error}

    def get_wireless_regtable(self):
        if self.is_connected:
            path = self.api.path("/interface/wireless/registration-table")
            return tuple(path)[0]
        else:
            return {"error": self.error}
