from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from anomaly.services import Anomalys

# Create your views here.

class AnomalysView(APIView):
	"""
	
	"""
	def get(self, request):
		"""
		"""
		res = Anomalys.getAnomalys()
		return Response(res.json())