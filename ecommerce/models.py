
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
    product_genre = models.CharField(max_length=30)
    product_number = models.IntegerField()
    product_description = models.TextField(max_length=300, null=True)
    product_stock = models.IntegerField()
    product_price = models.FloatField()
    warranty = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    page_number = models.IntegerField()
    author = models.CharField(max_length=50)
    image = models.ImageField(null=True)
    year = models.IntegerField()
    translator = models.CharField(max_length=50, null=True)
    editor = models.CharField(max_length=50, null=True)

