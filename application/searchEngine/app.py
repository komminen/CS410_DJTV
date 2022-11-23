from flask import Flask
from flask_restful import Resource, Api, reqparse
import json
app = Flask(__name__)
api = Api(app)

class Data(Resource):
    def get(self):
        f = open('movie_reviews_dataset.json')
        data = json.load(f)  # read json
        return {'data': data}, 200  # return data and 200 OK code
    
    def post(self):
        parser = reqparse.RequestParser()  # initialize

        parser.add_argument('query', required=True)

        args = parser.parse_args()

        print(args)

        return {'data': args}, 200

api.add_resource(Data, '/data')  # '/data' is our entry point

if __name__ == '__main__':
    app.run()  # run our Flask app