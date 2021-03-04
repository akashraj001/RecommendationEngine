# flask packages
from flask import jsonify
from flask_restful import Resource


# mongo-engine models


class Recommendation(Resource):
    def get(self):
        # output = AppSettingsModel.objects()
        return jsonify({'result': "got hit the testApi"})
