
from search import ma
from .models import GlobalDimension, GlobalDimensionValues

class GlobalDimensionValuesSchema(ma.Schema):
    
    class Meta:
        fields = ("id", "dimension","datasetId", "dataset")
        include_fk=True

class GlobalDimensionSchema(ma.Schema):
    
    id= ma.Integer()
    name = ma.String()
    published = ma.Boolean()
    values = ma.List(ma.Nested(GlobalDimensionValuesSchema()))
