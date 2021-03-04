from .testAPI import TestAPI


def create_routes(api):
    api.add_resource(TestAPI, '/test/')