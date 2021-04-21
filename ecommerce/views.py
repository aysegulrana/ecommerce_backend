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
from .serializers import cartSerializer
from .serializers import ordersSerializer
from .models import product
from .models import cart
from .models import orders


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

class delete(APIView):
    def get(self, request, pk, format=None):
        snippet = product.objects.filter(id = pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class update(APIView):
    def get(self,request,pk,x,count, format = None):
        if x == 1:
            product1 = product.objects.get(id=pk)
            product1.product_stock += count
            product1.save()
            return Response("Stock is updated")
        else:
            product1 = product.objects.get(id=pk)
            product1.product_stock -= count
            product1.save()
            return Response("Stock is updated")

class cart(APIView):
    def get(self, request):
        cart1 = cart.objects.all()
        serializer = cartSerializer(cart1, many=True)
        return Response(serializer.data)
class orders(APIView):
    def get(self, request):
        orders1 = orders.objects.all()
        serializer = ordersSerializer(orders1, many=True)
        return Response(serializer.data)