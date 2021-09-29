from search import db

class Something(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    salary = db.Column(db.Numeric)
    references = db.Column(db.String)

    def __repr__(self):
        return "(%r, %r, %r)" %(self.name,self.email,self.salary)

class Otherthing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datasetId = db.Column(db.Integer)
