from django.contrib import admin
from . models import user
from . models import product
admin.site.register(product)
admin.site.register(user)