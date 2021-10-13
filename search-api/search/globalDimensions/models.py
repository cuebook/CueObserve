from search import db

# For reference see tables below

class GlobalDimension(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False, unique=True)
    values = db.relationship('GlobalDimensionValues', backref='global_dimension', lazy=True, cascade="all, delete")
    published = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return "<GlobalDimension(name='%s')>" % (self.name)

class GlobalDimensionValues(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    datasetId = db.Column(db.Integer, nullable=False)
    dataset = db.Column(db.Text(), nullable=False)
    dimension = db.Column(db.Text(), nullable=False)
    globalDimensionId = db.Column(db.Integer, db.ForeignKey('global_dimension.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return "<GlobalDimensionValues(dimension='%s')>" % (self.dimension)