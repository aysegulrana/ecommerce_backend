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
from .serializers import cartSerializer
from .serializers import cartItemSerializer
from .serializers import orderSerializer, orderItemSerializer
from .models import cart, order, orderItem
from .models import cartItem


# from .models import orders"""

# Create your views here.
class userList(APIView):
    def get(self, request):
        try:
            user_mail = request.query_params["email"]
            if user_mail is not None:
                u1 = user.objects.get(email=user_mail)
                serializer = userSerializer(u1)
        except:
            u1 = user.objects.all()
            serializer = userSerializer(u1, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = userSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            """empty_cart=cart.objects.create(customer=request.data)
            s_cart=cartSerializer(data=empty_cart)
            s_cart.save()"""
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
        snippet = product.objects.filter(id=pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class update(APIView):
    def get(self, request, pk, x, count, format=None):
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

class cartAPI(APIView):
    """
    API endpoint that allows carts to be viewed or edited.
    """
    def get(self, request):

        user_id = request.query_params["email"]
        if user_id is not None:
            user1 = user.objects.get(email=user_id)
            cart1 = cart.objects.get(customer= user1)
            cart_items = cartItem.objects.filter(cart= cart1)
            serializer = cartItemSerializer(cart_items, many=True)
            return Response(serializer.data)
        else:
            return Response("Cart is empty")

    queryset = cart.objects.all()
    serializer_class = cartSerializer

class updateCart(APIView):
    def get(self, request, userID, productID,quantity):
        productToAdd = product.objects.get(id= productID)
        userCart = user.objects.get(email= userID)
        cartInProcess = cart.objects.get(customer=userCart)

        existing_cart_item = cartItem.objects.filter(cart=cartInProcess, product=productToAdd).first()
        # before creating a new cart item check if it is in the cart already
        # and if yes increase the quantity of that item
        if existing_cart_item:
            existing_cart_item.quantity += quantity
            existing_cart_item.save()
        else:
            new_cart_item = cartItem(cart=cartInProcess, product=productToAdd, quantity=quantity)
            new_cart_item.save()

        # return the updated cart to indicate success
        serializer = cartSerializer(cartInProcess)
        return Response(serializer.data)

class emptyCart(APIView):
    def get(self,request,cartID):
        currentCart=cart.objects.get(cart_id=cartID)
        try:
            items = cartItem.objects.filter(cart=currentCart)
        except Exception as e:
            print(e)
            return Response({'status': 'fail'})
        for i in items:
            i.delete()
        serializer = cartSerializer(currentCart)
        return Response(serializer.data)

class removeFromCart(APIView):
    def get(self, request, cartID, prodID):
        c = cart.objects.get(cart_id=cartID)
        p = product.objects.get(id=prodID)
        # u = user.objects.get(email=userID)
        try:
            item = cartItem.objects.get(cart=c, product=p)
        except Exception as e:
            print(e)
            return Response({'status': 'fail'})
                    # if removing an item where the quantity is 1, remove the cart item
                    # completely otherwise decrease the quantity of the cart item
        if item.quantity == 1:
            item.delete()
        else:
            item.quantity -= 1
            item.save()
                    # return the updated cart to indicate success
        serializer = cartSerializer(c)
        return Response(serializer.data)

class orderAPI(APIView):
    """
    API endpoint that allows carts to be viewed or edited.
    """
    def get(self, request):

        user_id = request.query_params["email"]
        if user_id is not None:
            user1 = user.objects.get(email=user_id)
            order1 = order.objects.get(customer= user1)
            order_items = orderItem.objects.filter(order= order1)
            serializer = orderItemSerializer(order_items, many=True)
            return Response(serializer.data)
        else:
                return Response("No orders")

    queryset = order.objects.all()
    serializer_class = orderSerializer

class updateOrder(APIView):
    def get(self, request, userID, productID, quantity):
        productToAdd = product.objects.get(id= productID)
        userOrder = user.objects.get(email= userID)
        orderInProcess = order.objects.get(customer=userOrder)

        existing_order_item = orderItem.objects.filter(order=orderInProcess, product=productToAdd).first()
        # before creating a new cart item check if it is in the cart already
        # and if yes increase the quantity of that item
        if existing_order_item:
            existing_order_item.quantity += quantity
            existing_order_item.save()
        else:
            new_order_item = orderItem(order=orderInProcess, product=productToAdd, quantity=quantity, state=0)
            new_order_item.save()

        # return the updated cart to indicate success
        serializer = orderSerializer(orderInProcess)
        return Response(serializer.data)

class orderStatus(APIView):
    def get(self, request, userID, productID, quantity):
        p = product.objects.get(id= productID)
        u = user.objects.get(email= userID)
        orderInProcess = order.objects.get(customer=u)

        order_item = orderItem.objects.filter(order=orderInProcess, product=p).first()
        if order_item:
            order_item.state += 1
            order_item.save()

        serializer = orderSerializer(orderInProcess)
        return Response(serializer.data)

class emptyOrder(APIView):
    def get(self,request,orderID):
        currentOrder=order.objects.get(order_id=orderID)
        try:
            items = orderItem.objects.filter(order=currentOrder)
        except Exception as e:
            print(e)
            return Response({'status': 'fail'})
        for i in items:
            i.delete()
        serializer = orderSerializer(currentOrder)
        return Response(serializer.data)

class removeFromOrder(APIView):
    def get(self, request, orderID, prodID):
        c = order.objects.get(order_id=orderID)
        p = product.objects.get(id=prodID)
        # u = user.objects.get(email=userID)
        try:
            item = orderItem.objects.get(order=c, product=p)
        except Exception as e:
            print(e)
            return Response({'status': 'fail'})
                    # if removing an item where the quantity is 1, remove the cart item
                    # completely otherwise decrease the quantity of the cart item
        if item.quantity == 1:
            item.delete()
        else:
            item.quantity -= 1
            item.save()
                    # return the updated cart to indicate success
        serializer = orderSerializer(c)
        return Response(serializer.data)
