from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
# Create your views here.
from admin.models import Advisor
from admin.serializers import Serial

@api_view(['POST'])
def create_advisor(request):
        data = JSONParser().parse(request)
        serializer = Serial(data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(data = {},safe = False,
            status = status.HTTP_200_OK)
        else : return JsonResponse(data = serializer.errors, safe = False,
        status = status.HTTP_400_BAD_REQUEST)
