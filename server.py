from flask import Flask
from flask_restful import Api
import resourses
import temp_resources

app = Flask(__name__)
api = Api(app)

cleaner = temp_resources.TempCleaner()
cleaner.start()

api.add_resource(resourses.Ping, "/ping/<address>")
api.add_resource(temp_resources.TempPing, "/temp/ping")
api.add_resource(resourses.QueueTraffic, "/queue/traffic/<name>")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
