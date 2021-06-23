from utils.apiResponse import ApiResponse
from anomaly.models import Anomaly

class Anomalys:
	"""
	"""

	@staticmethod
	def getAnomalys():
		res = ApiResponse("Error in getting anomalys")
		data = [{"name": "First anomaly"}]
		res.update(True, "Successfully retrieved anomaly", data)
		return res