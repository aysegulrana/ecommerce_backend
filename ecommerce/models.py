from django.db import models
from CS308 import settings


# Create your models here.
class user(models.Model):
    # REQUIRED_FIELDS=('email')
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    email = models.EmailField(max_length=30, primary_key=True)
    address = models.TextField(max_length=200, null=True)
    password = models.CharField(max_length=15)
    userType = models.IntegerField(default=0, auto_created=True)
    #userID = models.AutoField(primary_key=True)

    def __str__(self):
        return self.firstname


class product(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    product_model = models.CharField(max_length=30)  # hangi dizi filme ait
    product_size = models.IntegerField()
    product_description = models.TextField(max_length=300, null=True)
    product_stock = models.IntegerField()
    product_price = models.FloatField()
    warranty = models.CharField(max_length=50)
    seller = models.CharField(max_length=50)
    image = models.URLField(null=True)


# is this can be like one model with boolean variable indicating ordered yet
"""class cart(models.Model):
    # user = models.ForeignKey(user, on_delete=models.CASCADE)
    user = models.OneToOneField(
        user,
        on_delete=models.CASCADE,
        primary_key=True
    )
    # product_number = models.IntegerField()
    products = models.ManyToManyField(product, through="product_cart")"""


class cart(models.Model):
    """A model that contains data for a shopping cart."""
    customer = models.OneToOneField(
        user,
        related_name='cart', on_delete=models.CASCADE
    )
    cart_id = models.AutoField(primary_key=True)


class cartItem(models.Model):
    """A model that contains data for an item in the shopping cart."""
    cart = models.ForeignKey(
        cart,
        related_name='items',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    product = models.ForeignKey(
        product,
        related_name='items',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)

    def __unicode__(self):
        return '%s: %s' % (self.product.title, self.quantity)


"""class orders(models.Model):
    user = models.OneToOneField(
        user,
        on_delete=models.CASCADE,
        primary_key=True
    )
    order_number = models.IntegerField()
    date = models.DateField()
    products = models.ManyToManyField(product, through="product_orders")
    delivered = models.BooleanField()


class product_orders(models.Model):
    prod = models.ForeignKey(product, on_delete=models.CASCADE)
    order = models.ForeignKey(orders, on_delete=models.CASCADE)


class user_orders(models.Model):
    order = models.ForeignKey(orders, on_delete=models.CASCADE)
    usr = models.ForeignKey(user, on_delete=models.CASCADE)


class product_cart(models.Model):
    prod = models.ForeignKey(product, on_delete=models.CASCADE)
    c = models.ForeignKey(cart, on_delete=models.CASCADE)


class user_cart(models.Model):
    c = models.ForeignKey(cart, on_delete=models.CASCADE)
    usr = models.ForeignKey(user, on_delete=models.CASCADE)"""
