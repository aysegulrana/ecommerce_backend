from rest_framework import serializers
from .models import user, cart, cartItem, order, orderItem, comment
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


class cartSerializer(serializers.ModelSerializer):
    """Serializer for the Cart model."""

    customer = userSerializer(read_only=True)
    # used to represent the target of the relationship using its __unicode__ method
    items = serializers.StringRelatedField(many=True)

    class Meta:
        model = cart
        fields = '__all__'


class cartItemSerializer(serializers.ModelSerializer):
    """Serializer for the CartItem model."""

    cart = cartSerializer(read_only=True)
    product = productSerializer(read_only=True)

    class Meta:
        model = cartItem
        fields = '__all__'


class orderSerializer(serializers.ModelSerializer):
    """Serializer for the Cart model."""

    customer = userSerializer(read_only=True)
    # used to represent the target of the relationship using its __unicode__ method
    order_items = serializers.StringRelatedField(many=True)
    #seller=userSerializer(read_only=True)
    class Meta:
        model = order
        fields = '__all__'


class orderItemSerializer(serializers.ModelSerializer):
    """Serializer for the CartItem model."""

    order = orderSerializer(read_only=True)
    product = productSerializer(read_only=True)

    class Meta:
        model = orderItem
        fields = '__all__'

class commentSerializer(serializers.ModelSerializer):
    product = productSerializer(read_only=True)
    user = userSerializer(read_only=True)

    class Meta:
        model = comment
        fields = '__all__'