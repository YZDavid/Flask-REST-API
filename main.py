from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

video_put_args = reqparse.RequestParser()
video_put_args.add_argument('name', type=str, help='Name of the video', required=True)
video_put_args.add_argument('likes', type=int, help='Likes on the video', required=True)
video_put_args.add_argument('views', type=int, help='Views on the video', required=True)

videos = {}

database = {
    1: ['abc', 123],
    2: ['xyz', 789],
    3: ['testing', 69420]
}


class Video(Resource):
    def get(self, video_id):
        return {video_id: videos[video_id]}
    
    def post(self, video_id):
        return {'data': 'Sent via POST'}
    
    def put(self, video_id):
        args = video_put_args.parse_args()
        print(type(video_id), video_id)
        videos[video_id] = args
        return videos[video_id], 201
    
class Home(Resource):
    def get(self):
        return "Homepage"

api.add_resource(Video, "/video/<int:video_id>", "/<int:video_id>")
api.add_resource(Home, '/', '/home')

if __name__ == '__main__':
    app.run(debug=True)

