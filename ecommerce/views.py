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
# from .serializers import ordersSerializer
from .models import cart
# from rest_framework.decorators import detail_route
# from rest_framework.decorators import list_route
from .models import cartItem


# from .models import orders"""

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


"""class cart(APIView):
    def get(self, request):
        cart1 = cart.objects.all()
        serializer = cartSerializer(cart1, many=True)
        return Response(serializer.data)
class orders(APIView):
    def get(self, request):
        orders1 = orders.objects.all()
        serializer = ordersSerializer(orders1, many=True)
        return Response(serializer.data)"""


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

        existing_cart_item = cartItem.objects.filter(cart=cart, product=productToAdd).first()
        # before creating a new cart item check if it is in the cart already
        # and if yes increase the quantity of that item
        if existing_cart_item:
            existing_cart_item.quantity += quantity
            existing_cart_item.save()
        else:
            new_cart_item = cartItem(cart=cart, product=productToAdd, quantity=quantity)
            new_cart_item.save()

        # return the updated cart to indicate success
        serializer = cartSerializer(cart)
        return Response(serializer.data)




        """  def add_to_cart(self, request, pk=None):
        Add an item to a user's cart.
        Adding to cart is disallowed if there is not enough inventory for the
        product available. If there is, the quantity is increased on an existing
        cart item or a new cart item is created with that quantity and added
        to the cart.
        Parameters
        ----------
        request: request
        Return the updated cart.
        
        cart = self.get_object()
        try:
            prod = product.objects.get(
                pk=request.data['id']
            )  # we get product's id
            quantity = int(request.data['product_stock'])
        except Exception as e:
            print(e)
            return Response({'status': 'fail'})

        # Disallow adding to cart if available inventory is not enough
        # this is frontend's job??
        if product.available_inventory <= 0 or product.available_inventory - quantity < 0:
            print ("There is no more product available")
            return Response({'status': 'fail'})

        existing_cart_item = cartItem.objects.filter(cart=cart, product=prod).first()
        # before creating a new cart item check if it is in the cart already
        # and if yes increase the quantity of that item
        if existing_cart_item:
            existing_cart_item.quantity += quantity
            existing_cart_item.save()
        else:
            new_cart_item = cartItem(cart=cart, product=prod, quantity=quantity)
            new_cart_item.save()

        # return the updated cart to indicate success
        serializer = cartSerializer(cart)
        return Response(serializer.data)

    # @detail_route(methods=['post', 'put'])
    def remove_from_cart(self, request, pk=None):
        Remove an item from a user's cart.
        Like on the Everlane website, customers can only remove items from the
        cart 1 at a time, so the quantity of the product to remove from the cart
        will always be 1. If the quantity of the product to remove from the cart
        is 1, delete the cart item. If the quantity is more than 1, decrease
        the quantity of the cart item, but leave it in the cart.
        Parameters
        ----------
        request: request
        Return the updated cart.
        
        cart = self.get_object()
        try:
            prod = product.objects.get(
                pk=request.data['id']
            )
        except Exception as e:
            print(e)
            return Response({'status': 'fail'})

        try:
            cart_item = cartItem.objects.get(cart=cart, product=prod)
        except Exception as e:
            print(e)
            return Response({'status': 'fail'})

        # if removing an item where the quantity is 1, remove the cart item
        # completely otherwise decrease the quantity of the cart item
        if cart_item.quantity == 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()

        # return the updated cart to indicate success
        serializer = cartSerializer(cart)
        return Response(serializer.data)


class CartItemViewSet(APIView):
    
    API endpoint that allows cart items to be viewed or edited.
    
    queryset = cartItem.objects.all()
    serializer_class = cartItemSerializer 
    
    """
