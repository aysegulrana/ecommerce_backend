from rest_framework import serializers
from .models import user
from .models import product
from .models import cart
from .models import orders


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = '__all__'


class productSerializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = '__all__'

class ordersSerializer(serializers.ModelSerializer):
    class Meta:
        model = orders
        fields = '__all__'


class cartSerializer(serializers.ModelSerializer):
    class Meta:
        model = cart
        fields = '__all__'
