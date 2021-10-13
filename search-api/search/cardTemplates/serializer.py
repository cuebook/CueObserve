from search import ma
from search.cardTemplates.models import SearchCardTemplate

class SearchCardTemplateSchema(ma.Schema):

    id = ma.Integer()
    templateName = ma.String()
    title = ma.String()
    bodyText = ma.String()
    supportedVariables = ma.String()