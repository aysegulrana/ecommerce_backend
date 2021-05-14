import decimal

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
from django.shortcuts import get_object_or_404

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
            u=user.objects.get(email=serializer.data.get('email',None))
            empty_cart=cart.objects.create(customer=u)
            s_cart=cartSerializer(data=empty_cart)
            if s_cart.is_valid():
                s_cart.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class deleteUser(APIView):
    def get(self, request, mail, format=None):
        snippet = user.objects.filter(email=mail)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class changeAddress(APIView):
    def get(self,request,mail, new_address):
        user1 = user.objects.get(email=mail)
        user1.address = new_address
        user1.save()
        return Response("Address is changed")

class changeName(APIView):
    def get(self,request,mail,name,surname):
        user1 = user.objects.get(email=mail)
        user1.firstname= name
        user1.lastname= surname
        user1.save()
        return Response("User name is changed")

class changePassword(APIView):
    def get(self,request,mail,new_pass):
        user1 = user.objects.get(email=mail)
        user1.password = new_pass
        user1.save()
        return Response("Password is changed")

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

#delete product
class delete(APIView):
    def get(self, request, pk, format=None):
        snippet = product.objects.filter(id=pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#change product stock
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
            order1 = get_object_or_404(order,customer= user1)
            order_items = orderItem.objects.filter(order= order1)
            serializer = orderItemSerializer(order_items, many=True)
            return Response(serializer.data)

        else:
            return Response("No orders")

    queryset = order.objects.all()
    serializer_class = orderSerializer

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

#OLMADI BU
# cart'ı order'a dönüştürmek için
class cartToOrder(APIView):
    def get(self, request, id):
        u = user.objects.get(email=id)
        c = cart.objects.get(customer=u)
        o = order.objects.get(customer=u)
        items = cartItem.objects.filter(cart=c)
        s_item = cartItemSerializer(items, many=True)
        for item in s_item.data:
            #s = cartItemSerializer(data=item)
            #if s.is_valid():
                #s.save()

            p = item.get('product',None) #get product from cart item
            p=product.objects.get(id=p.get('id',None))
            q = item.get('quantity', None)  #get quantity from cart item

            order_item =orderItem.objects.create(product=p,order=o,quantity=q,state=0)
            o.total += decimal.Decimal(p.product_price * q) #find how much this cart item adds to the total order payment
            #saving the created order item
            o.save()
            s_order = orderItemSerializer(data=order_item)
            if s_order.is_valid():
                s_order.save()
            #item.delete() #remove from the cart
        order_items = orderItem.objects.filter(order=o)
        serializer = orderItemSerializer(order_items, many=True)
        return Response(serializer.data)

        """serializer = cartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            current_cart=serializer.data.get('cart',None) #we got cart from cart item
            current_user=current_cart.get('customer',None) #user from cart
            prod=serializer.data.get('product',None) #product from cart item
            quant=serializer.data.get('quantity',None) #quantity from cart item
            current_order=order.objects.get(customer=current_user)
            current_order.total+=(prod.product_price*quant)
            #***order from user yoksa yeni order mı create etmeliyim?

            item=orderItem.objects.create(product=prod,order=current_order,quantity=quant,state=0)
            s_order=orderItemSerializer(data=item)

            if s_order.is_valid():
                s_order.save()
                return Response(s_order.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)"""

#API for cancelling an existing order. Takes order ID as parameter
class cancelOrder(APIView):
    def get(self, request, ID):
        snippet = order.objects.filter(order_id=ID)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class cancelOrderItem(APIView):
    def get(self, request, prodID):
        snippet = orderItem.objects.filter(product.objects.get(id=prodID))
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)