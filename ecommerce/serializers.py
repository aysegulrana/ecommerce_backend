from rest_framework import serializers
from .models import user
from .models import product


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = '__all__'


class productSerializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = '__all__'
