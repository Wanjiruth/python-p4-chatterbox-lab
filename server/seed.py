# server/seed.py

from app import app
from models import db, User, Task, Assignment, Message
from datetime import datetime
from faker import Faker

fake = Faker()

with app.app_context():
    db.create_all()

    # Create users
    users = []
    for _ in range(10):
        user = User(
            name=fake.name(),
            email=fake.email(),
            password_hash=fake.password()
        )
        users.append(user)
    db.session.add_all(users)
    db.session.commit()

    # Create tasks
    tasks = []
    for _ in range(20):
        task = Task(
            title=fake.sentence(),
            description=fake.paragraph(),
            due_date=fake.future_date(),
            user_id=fake.random_element(users).id
        )
        tasks.append(task)
    db.session.add_all(tasks)
    db.session.commit()

    # Create assignments
    assignments = []
    statuses = ['Not Started', 'In Progress', 'Completed']
    for task in tasks:
        assignment = Assignment(
            task_id=task.id,
            user_id=fake.random_element(users).id,
            status=fake.random_element(statuses)
        )
        assignments.append(assignment)
    db.session.add_all(assignments)
    db.session.commit()

    # Create messages
    messages = []
    for _ in range(15):
        message = Message(
            body=fake.sentence(),
            username=fake.user_name(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        messages.append(message)
    db.session.add_all(messages)
    db.session.commit()
