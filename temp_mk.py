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
