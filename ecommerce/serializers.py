from rest_framework import serializers
from .models import user
from .models import product
"""from .models import cart
from .models import orders
from .models import product_cart
from .models import product_orders
from .models import user_cart
from .models import user_orders"""


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = '__all__'


class productSerializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = '__all__'


"""class ordersSerializer(serializers.ModelSerializer):
    class Meta:
        model = orders
        fields = '__all__'


class cartSerializer(serializers.ModelSerializer):
    class Meta:
        model = cart
        fields = '__all__'


class user_ordersSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_orders
        fields = '__all__'


class product_ordersSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_orders
        fields = '__all__'


class user_cartSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_cart
        fields = '__all__'


class product_cartSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_cart
        fields = '__all__'"""
