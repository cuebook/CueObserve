from utils.apiResponse import ApiResponse
from anomaly.models import Connection
from dbConnections.dbConnection import BigQueryConnection


class Querys:
	"""
	Services for querying connection
	"""

	@staticmethod
	def runQuery(connectionType, connectionParams, query, limit=True):
		res = ApiResponse("Error in getting data")
		data = None
		if connectionType == "BigQuery":
			file = connectionParams['file']
			data = BigQueryConnection.fetchData(file, query, limit=True)

		res.update(True, "Successfully retrieved data", data)
		return res
