import os
from librouteros import connect
from librouteros.login import plain

MAIN_HOST = os.environ.get("MAIN_HOST")
MAIN_USERNAME = os.environ.get("MAIN_USERNAME")
MAIN_PASSWORD = os.environ.get("MAIN_PASSWORD")
MAIN_PORT = os.environ.get("MAIN_PORT")

MK = connect(host=MAIN_HOST, username=MAIN_USERNAME, password=MAIN_PASSWORD, port=MAIN_PORT, login_methods=plain)
