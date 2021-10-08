
from search import ma
from search.globalDimensions.models import GlobalDimension, GlobalDimensionValues

class GlobalDimensionValuesSchema(ma.Schema):
    
    class Meta:
        fields = ("id", "dimensionName","datasetId", "datasetName")
        include_fk=True


class GlobalDimensionSchema(ma.Schema):
    
    id= ma.Integer()
    name = ma.String()
    values = ma.List(ma.Nested(GlobalDimensionValuesSchema(only=("dimensionName",))))



# globaldimension_schema = GlobalDimensionSchema()
# globaldimensions_schema = GlobalDimensionSchema(many=True)

# globaldimensionValue_schema = GlobalDimensionValuesSchema()
# globaldimensionValues_schema = GlobalDimensionValuesSchema(many=True)