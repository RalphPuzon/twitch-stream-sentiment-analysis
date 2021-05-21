from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import os, sys, json
from datetime import datetime as d

app = Flask(__name__)
api = Api(app)
rec_root = os.path.join(os.path.realpath(__file__), '../records')

class MsgLogger(Resource):
    def post(self):
        pdt = json.loads(request.get_data().decode("UTF-8"))
        channel = pdt["channel"][1:]
        date = d.now().strftime("%m-%d-%Y")
        filename = os.path.join(rec_root, channel, str(date), "_x_" + channel + ".json")
        try:
            if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))
            with open(filename, 'a') as json_file:
                json.dump(pdt, json_file)
                json_file.write("\n")
            returnJSON = {
                "message": "write successful",
                }

            return jsonify(returnJSON)

        except:
            e = sys.exc_info()[0]
            returnJSON = {
                "message": "A parsing error has occured",
                "data received": pdt,
                "error": e
            }

            return jsonify(returnJSON)

api.add_resource(MsgLogger, "/writerinput")

if __name__ == "__main__":
    app.run(port=5001, debug=True)