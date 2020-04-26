from flask_restful import reqparse


class PARSER:
    def __init__(self):
        self.parser = reqparse.RequestParser()

        self.parser.add_argument('host', type=str)
        self.parser.add_argument('username', type=str)
        self.parser.add_argument('password', type=str)
        self.parser.add_argument('port', type=int)
        self.parser.add_argument('address', type=str)
