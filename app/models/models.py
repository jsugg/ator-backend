from app import db

class TestSuite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256))
    # Relationships and additional fields

class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_suite_id = db.Column(db.Integer, db.ForeignKey('test_suite.id'), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256))
    # Additional fields and relationships
