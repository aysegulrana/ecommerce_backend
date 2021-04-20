from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import user
from .serializers import userSerializer
from .serializers import productSerializer
from .models import product


# Create your views here.
class userList(APIView):
    def get(self, request):
        user1 = user.objects.all()
        serializer = userSerializer(user1, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = userSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class productList(APIView):
    def get(self, request):
        try:
            product_id = request.query_params["id"]
            if product_id is not None:
                product1 = product.objects.get(id=product_id)
                serializer = productSerializer(product1)

        except:
            try:
                product_category = request.query_params["product_model"]
                if product_category is not None:
                    product1 = product.objects.filter(product_model=product_category)
                    serializer = productSerializer(product1, many=True)

            except:
                product1 = product.objects.all()
                serializer = productSerializer(product1, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = productSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
