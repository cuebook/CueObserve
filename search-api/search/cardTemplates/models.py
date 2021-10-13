from search import db

class SearchCardTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    templateName = db.Column(db.String)
    title = db.Column(db.String)
    bodyText = db.Column(db.String)
    supportedVariables = db.Column(db.String)

    def __repr__(self):
        return self.templateName
