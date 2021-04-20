
from django.db import models

# Create your models here.
class user(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    email = models.EmailField(max_length=30, primary_key=True)
    address = models.TextField(max_length=200, null=True)
    password = models.CharField(max_length=15)

    def __str__(self):
        return self.firstname

class product(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    product_model = models.CharField(max_length=30) #hangi dizi filme ait
    product_size = models.IntegerField()
    product_description = models.TextField(max_length=300, null=True)
    product_stock = models.IntegerField()
    product_price = models.FloatField()
    warranty = models.CharField(max_length=50)
    seller = models.CharField(max_length=50)
    image = models.ImageField(null=True)

