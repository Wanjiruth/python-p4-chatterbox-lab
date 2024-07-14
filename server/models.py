# server/models.py

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin



db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    tasks = db.relationship('Task', backref='user', lazy=True)
    assignments = db.relationship('Assignment', backref='user', lazy=True)
    
    serialize_rules = ('-tasks.user', '-assignments.user')

    def __repr__(self):
        return f"<User {self.name}>"

class Task(db.Model, SerializerMixin):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    assignments = db.relationship('Assignment', backref='task', lazy=True)
    
    serialize_rules = ('-user.tasks', '-assignments.task', '-assignments.user')

    def __repr__(self):
        return f"<Task {self.title}>"

class Assignment(db.Model, SerializerMixin):
    __tablename__ = 'assignments'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    
    serialize_rules = ('-task.assignments', '-user.assignments', '-task.user', '-user.tasks')

    def __repr__(self):
        return f"<Assignment {self.id} - Task {self.task_id} - User {self.user_id} - Status {self.status}>"

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Message {self.body[:20]} by {self.username}>"
