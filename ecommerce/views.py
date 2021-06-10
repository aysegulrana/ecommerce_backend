import decimal

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import user, comment
from .serializers import userSerializer, commentSerializer
from .serializers import productSerializer
from .models import product
from .serializers import cartSerializer
from .serializers import cartItemSerializer
from .serializers import orderSerializer, orderItemSerializer
from .models import cart, order, orderItem
from .models import cartItem
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
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
            subject = "Your account is active!"
            message = "You have successfully registered to our website."
            #from_email = settings.EMAIL_HOST_USER
            to_list = [serializer.data.get('email',None)]
            print(to_list)
            send_mail(subject,message,None,to_list,fail_silently=True)

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
#float update edemiyor integer ekleyebiliyoruz
class updatePrice(APIView):
    def get(self, request, id, x, price, format=None):

        if x==1:
            product1 = product.objects.get(id=id)
            product1.product_price += price
            product1.save()
            return Response("Price is updated")
        else:
            product1 = product.objects.get(id=id)
            product1.product_price -= price
            product1.save()
            return Response("Price is updated")

        # Notifying registered users of price updates

        subject = "Price Update"
        message = "Price for " + product1.product_name + " is updated. New price is" + product1.product_price
        from_email = settings.EMAIL_HOST_USER
        userList = user.get.all()
        to_list = []
        for u in userList:
            to_list.append(u.email)
        send_mail(subject,message,from_email,to_list,fail_silently=True)

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

    def post(self, request):
        serializer = cartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

class totalCart(APIView):
    def get(self, request, cartID):
        c=cart.objects.get(cart_id=cartID)
        total=0
        try:
            items = cartItem.objects.filter(cart=c)
        except Exception as e:
            print(e)
            return Response({'status': 'fail'})
        s_item = cartItemSerializer(items, many=True)
        for item in s_item.data:
            p = item.get('product', None)  # get product from cart item
            px = product.objects.get(id=p.get('id', None))
            total+=px.product_price
        return Response(total)

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

    def post(self, request):
        serializer = orderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#orderItem modelinden status field'ı kaldırıp order modeline ekledik.
"""class orderStatus(APIView):
    def get(self, request, userID, productID, quantity):
        p = product.objects.get(id= productID)
        u = user.objects.get(email= userID)
        orderInProcess = order.objects.get(customer=u)

        order_item = orderItem.objects.filter(order=orderInProcess, product=p).first()
        if order_item:
            order_item.state += 1
            order_item.save()

        serializer = orderSerializer(orderInProcess)
        return Response(serializer.data)"""

#cart'ı order'a dönüştürmek için
class cartToOrder(APIView):
    def get(self, request, id):
        u = user.objects.get(email=id)
        c = cart.objects.get(customer=u)
        o = order.objects.get(customer=u)
        try:
            items = cartItem.objects.filter(cart=c)
        except Exception as e:
            print(e)
            return Response({'status': 'fail'})

        s_item = cartItemSerializer(items, many=True)
        for item in s_item.data:
            p = item.get('product',None) #get product from cart item
            p=product.objects.get(id=p.get('id',None))
            q = item.get('quantity', None)  #get quantity from cart item

            existing_order_item = orderItem.objects.filter(order=o, product=p).first()
            if existing_order_item:
                existing_order_item.quantity += q
                existing_order_item.save()
            else:
                order_item = orderItem.objects.create(product=p,order=o,quantity=q)
                s_order = orderItemSerializer(data=order_item)
                if s_order.is_valid():
                    s_order.save()
            o.total += decimal.Decimal(p.product_price * q) #find how much this cart item adds to the total order payment
            #saving the changes in order
            o.save()

            #Sending the invoice

            subject = "Invoice"
            message = "Thank you for your order. You may find the invoice attached."
            from_email = settings.EMAIL_HOST_USER
            to_list = [id]
            send_mail(subject,message,from_email,to_list,fail_silently=True)

        for i in items:
            i.delete()

        order_items = orderItem.objects.filter(order=o)
        serializer = orderItemSerializer(order_items, many=True)
        return Response(serializer.data)


#API for cancelling an existing order. Takes order ID as parameter
class cancelOrder(APIView):
    def get(self, request, ID):
        snippet = order.objects.filter(order_id=ID)
        snippet.order_status = 4
        snippet.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class cancelOrderItem(APIView):
    def get(self, request, prodID,orderID):
        o=order.objects.get(order_id=orderID)
        p=product.objects.get(id=prodID)
        snippet = orderItem.objects.filter(order=o,product=p)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class getAllComments(APIView):
    def get(self, request,pid):
        try:
            c1 = comment.objects.filter(productCommenting= pid)
            serializer = commentSerializer(c1, many=True)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)

        """
           try:
               related_product = request.query_params["id"]
               if related_product is not None:
                   p1 = product.objects.get(id=related_product)
                   c1=comment.objects.get(productCommenting=p1,many=True)
                   serializer = commentSerializer(c1)
           except:
               p1 = product.objects.get(id=related_product)
               c1 = comment.objects.all()
               serializer = commentSerializer(p1,many=True)
           return Response(serializer.data)"""

class getCommentById(APIView):
    def get(self, request, comment_id):
        c1 = comment.objects.get(id=comment_id)
        serializer = commentSerializer(c1)
        return Response(serializer.data)

class postComment(APIView):
    def post(self, request):
        serializer = commentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class deleteComment(APIView):
    def get(self, request, comment_id, format=None):
        snippet = comment.objects.filter(id=comment_id)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class approveComment(APIView):
    def get(self, request, comment_id):
        c=comment.objects.get(id=comment_id)
        c.isApproved=1
        c.save()
        serializer = commentSerializer(c)
        return Response(serializer.data)

class rate(APIView):
    def get(self,request, productID, rate):
        p=product.objects.get(id=productID)
        x = (p.rate * p.rate_number) + float(rate)
        p.rate_number+=1
        p.rate=x/p.rate_number
        p.save()
        return Response("Rate is updated")

#API for viewing all invoices within a date range.
class viewOrders(APIView):
    def get(self,request, start_date, end_date, seller):
        orders = order.objects.filter(seller=seller, date__range=[start_date, end_date])
        serializer = orderSerializer(orders, many=True)
        return Response(serializer.data)

class requestRefund(APIView):
    def get(self, orderID):
        refund_order = order.objects.filter(order_id = orderID)
        refund_order.order_status = 3

        #inform seller about refund request
        subject = "Refund"
        message = "Customer " +  refund_order.customer.firstname + refund_order.customer.lastname + "wants to cancel order with id " + orderID
        from_email = settings.EMAIL_HOST_USER
        to_list = [refund_order.seller.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return Response(status=status.HTTP_204_NO_CONTENT)




