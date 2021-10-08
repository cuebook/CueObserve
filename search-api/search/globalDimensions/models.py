from search import db

# For reference see tables below

class GlobalDimension(db.Model):
    __tablename__ = 'globaldimension'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False, unique=True)
    values = db.relationship('GlobalDimensionValues', backref='globaldimension', lazy=True)
    published = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return "<GlobalDimension(name='%s')>" % (self.name)

class GlobalDimensionValues(db.Model):
    __tablename__ = 'globaldimensionvalues'

    id = db.Column(db.Integer, primary_key=True)
    datasetId = db.Column(db.Integer, nullable=False)
    dataset = db.Column(db.Text(), nullable=False)
    dimension = db.Column(db.Text(), nullable=False)
    globalDimensionId = db.Column(db.Integer, db.ForeignKey('globaldimension.id'), nullable=False)

    def __repr__(self):
        return "<GlobalDimensionValues(dimensionName='%s')>" % (self.dimensionName)