from django.contrib import admin
from . models import user
from . models import product
from . models import cart
from . models import orders
admin.site.register(product)
admin.site.register(user)
admin.site.register(cart)
admin.site.register(orders)