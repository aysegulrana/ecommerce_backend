from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import user
from .serializers import userSerializer

# Create your views here.
class userList(APIView):
    def get(self, request):
        user1 = user.objects.all()
        serializer = userSerializer(user1, many=True)
        return Response(serializer.data)
