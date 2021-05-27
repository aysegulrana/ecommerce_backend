from django.contrib import admin
from .models import user, cart, cartItem, comment
from . models import product
from .models import order
from .models import orderItem

admin.site.register(product)
admin.site.register(user)
admin.site.register(cart)
admin.site.register(cartItem)
admin.site.register(order)
admin.site.register(orderItem)
admin.site.register(comment)