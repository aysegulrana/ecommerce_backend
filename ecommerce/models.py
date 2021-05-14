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
    #userID = models.AutoField(unique=True)

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

class order(models.Model):
    customer = models.ForeignKey(
        user,
        related_name='orders',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    total = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_id = models.AutoField(primary_key=True)

class orderItem(models.Model):
    """A model that contains data for an item in an order."""
    order = models.ForeignKey(
        order,
        related_name='order_items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        product,
        related_name='order_items',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(null=True, blank=True)
    state=models.IntegerField()

    #order'da total price artırılması yazılacak.
    #def __unicode__(self):
        #return '%s: %s' % (self.product.title, self.quantity)