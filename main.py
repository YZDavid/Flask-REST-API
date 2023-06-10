from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'data': 'Hello World'}
    
class HelloAgain(Resource):
    def get(self):
        key = 'data'
        val = 'updog'
        return {key:val}

    
api.add_resource(HelloWorld, "/")
api.add_resource(HelloAgain, '/heyo')

if __name__ == '__main__':
    app.run(debug=True)

