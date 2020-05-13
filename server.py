from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import resources
import temp_resources

app = Flask(__name__)
api = Api(app)

cleaner = temp_resources.TempCleaner()
cleaner.start()

api.add_resource(resources.Ping, "/ping/<address>")
api.add_resource(resources.ArpPing, "/pingarp")
api.add_resource(resources.InterfaceTraffic, "/interface/traffic")
api.add_resource(resources.QueueTraffic, "/queue/traffic/<name>")

api.add_resource(temp_resources.TempPing, "/temp/ping")
api.add_resource(temp_resources.TempInterfaceTraffic, "/temp/interface/traffic")


cors = CORS(app, resources={r"/*": {"origins": "*"}})
if __name__ == "__main__":
    app.run(host='0.0.0.0')
