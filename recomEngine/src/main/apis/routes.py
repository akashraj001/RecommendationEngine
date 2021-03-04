from .testAPI import TestAPI
from .activityRecommendation import Recommendation

def create_routes(api):
    # api.add_resource(TestAPI, '/test/')
    api.add_resource(Recommendation, '/recommendation/')