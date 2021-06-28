import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpRequest

from anomaly.services import Anomalys
from anomaly.services import Connections

# Create your views here.

class AnomalysView(APIView):
	"""
	
	"""
	def get(self, request):
		"""
		"""
		res = Anomalys.getAnomalys()
		return Response(res.json())

# TODO 
# class for connections
@api_view(["GET", "POST"])
def connections(request: HttpRequest) -> Response:
    """
    Method to get or add connection
    :param request: HttpRequest
    """
    if request.method == "GET":
        res = Connections.getConnections()
        return Response(res.json())
    elif request.method == "POST":
        res = Connections.addConnection(request.data)
        return Response(res.json())


@api_view(["GET", "PUT", "DELETE"])
def connection(request: HttpRequest, connection_id: int) -> Response:
    """
    Method for crud operations on a single connection
    :param request: HttpRequest
    :param connection_id: Connection Id
    """
    if request.method == "GET":
        res = Connections.getConnection(connection_id)
        return Response(res.json())
    elif request.method == "DELETE":
        res = Connections.removeConnection(connection_id)
        return Response(res.json())
    elif request.method == "PUT":
        res = Connections.updateConnection(connection_id, request.data)
        return Response(res.json())


@api_view(["GET", "POST"])
def connectionTypes(request: HttpRequest) -> Response:
    """
    Method to get all connection types
    :param request: HttpRequest
    """
    if request.method == "GET":
        res = Connections.getConnectionTypes()
        return Response(res.json())
