from django.contrib import admin
from . models import user
from . models import product
"""from . models import cart
from . models import orders
from . models import product_cart
from . models import product_orders
from . models import user_cart
from . models import user_orders"""

admin.site.register(product)
admin.site.register(user)
"""admin.site.register(cart)
admin.site.register(orders)
admin.site.register(product_cart)
admin.site.register(product_orders)
admin.site.register(user_cart)
admin.site.register(user_orders)"""