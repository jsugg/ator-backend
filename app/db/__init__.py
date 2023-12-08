from app import create_app
from app.extensions import db

app = create_app('development')

with app.app_context():
    db.create_all()
