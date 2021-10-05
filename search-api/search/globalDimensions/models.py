from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)


# For reference see tables below

class GlobalDimension(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False, unique=True)
    dimensionValues = db.relationship('GlobalDimensionValues', backref="globaldimension", lazy=True)


class GlobalDimensionValues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datasetId = db.Column(db.Integer, nullable=False)
    dimensionName = db.Column(db.Text(), nullable=False)
    globalDimensionId = db.Column(db.Integer,  db.ForeignKey('globaldimension.id'), nullable=False)
