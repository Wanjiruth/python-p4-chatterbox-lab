# server/app.py

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from datetime import datetime
from models import db, User, Task, Assignment, Message

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

@app.route("/")
def index():
    return "<h1>Task Management App</h1>"

class MessagesResource(Resource):
    def get(self):
        messages = Message.query.all()
        return [message.to_dict() for message in messages], 200

    def post(self):
        data = request.get_json()
        try:
            new_message = Message(
                body=data['body'],
                username=data['username']
            )
            db.session.add(new_message)
            db.session.commit()
            return new_message.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"errors": [str(e)]}, 400

class MessageResource(Resource):
    def get(self, id):
        message = db.session.get(Message, id)
        if message:
            return message.to_dict(), 200
        return {"error": "Message not found"}, 404

    def patch(self, id):
        message = db.session.get(Message, id)
        if message:
            data = request.get_json()
            message.body = data.get('body', message.body)
            message.updated_at = datetime.utcnow()
            db.session.commit()
            return message.to_dict(), 200
        return {"error": "Message not found"}, 404

    def delete(self, id):
        message = db.session.get(Message, id)
        if message:
            db.session.delete(message)
            db.session.commit()
            return '', 204
        return {"error": "Message not found"}, 404

api.add_resource(MessagesResource, '/messages')
api.add_resource(MessageResource, '/messages/<int:id>')

if __name__ == "__main__":
    app.run(port=5555, debug=True)
