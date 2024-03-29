"""CS308 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from ecommerce import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', views.userList.as_view()),
    path('deleteuser/<str:mail>/', views.deleteUser.as_view()),
    path('product/', views.productList.as_view()),
    path('delete/<int:pk>/', views.delete.as_view()),
    path('update/<int:pk>/<int:x>/<int:count>/', views.update.as_view()),
    path('updateprice/<int:id>/<int:x>/<int:price>/', views.updatePrice.as_view()),
    path('cartAPI/', views.cartAPI.as_view()),
    path('updateCart/<str:userID>/<int:productID>/<int:quantity>/', views.updateCart.as_view()),
    path('totalCart/<str:cartID>/', views.totalCart.as_view()),
    path('removeFromCart/<int:cartID>/<int:prodID>/', views.removeFromCart.as_view()),
    path('emptyCart/<int:cartID>/', views.emptyCart.as_view()),
    path('orderAPI/', views.orderAPI.as_view()),
    path('cancelOrderItem/<int:prodID>/<int:orderID>/', views.cancelOrderItem.as_view()),
    path('changeAddress/<str:mail>/<str:new_address>/', views.changeAddress.as_view()),
    path('changeName/<str:mail>/<str:name>/<str:surname>/', views.changeName.as_view()),
    path('changePassword/<str:mail>/<str:new_pass>/', views.changePassword.as_view()),
    path('cartToOrder/<str:id>/', views.cartToOrder.as_view()),
    path('rate/<int:productID>/<int:rate>/', views.rate.as_view()),
    path('postComment/', views.postComment.as_view()),
    path('deleteComment/<int:comment_id>/', views.deleteComment.as_view()),
    path('approveComment/<int:comment_id>/', views.approveComment.as_view()),
    path('getCommentById/<int:comment_id>/', views.getCommentById.as_view()),
    path('getAllComments/<int:pid>/', views.getAllComments.as_view()),
    path('getApprovedComments/<int:pid>/', views.getAllApprovedComments.as_view()),
    path('requestRefund/<int:orderID>/', views.requestRefund.as_view()),
]