from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Video(name = {self.name}, views = {self.views}, likes = {self.likes})'

db.create_all()

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

video_put_args = reqparse.RequestParser()
video_put_args.add_argument('name', type=str, help='Name of the video', required=True)
video_put_args.add_argument('likes', type=int, help='Likes on the video', required=True)
video_put_args.add_argument('views', type=int, help='Views on the video', required=True)

video_patch_args = reqparse.RequestParser()
video_patch_args.add_argument('name', type=str, help='Name of the video')
video_patch_args.add_argument('likes', type=int, help='Likes on the video')
video_patch_args.add_argument('views', type=int, help='Views on the video')

class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message='Video ID not found')
        return result
    
    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message='Video ID already exists')
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201
    
    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_patch_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message='Video ID not found')

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']
        
        db.session.commit()

        return result

    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if result is None:
            abort(404, message='Video ID not found', status=404)
        db.session.delete(result)
        db.session.commit()
        return '', 200
    
class Home(Resource):
    def get(self):
        return "Homepage"

api.add_resource(Video, "/video/<int:video_id>", "/<int:video_id>")
api.add_resource(Home, '/', '/home')

if __name__ == '__main__':
    app.run(debug=True)

