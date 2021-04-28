import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import product
from ..serializers import productSerializer
from ..models import user
from ..serializers import userSerializer
from ..models import cart
from ..serializers import cartSerializer
from ..models import orders
from ..serializers import ordersSerializer


# initialize the APIClient app
client = Client()

class GetAllUsersTest(TestCase):
    """ Test module for GET all puppies API """

    def setUp(self):
        user.objects.create(
            firstname='Aysegul', lastname='Erdemli', email='aysegulrana@sabanciuniv.edu', address='Izmit'
        ,password='admin')
        user.objects.create(
            firstname='Dilara', lastname='Tekinoglu', email='dilaramemis@sabanciuniv.edu', address='Istanbul'
        ,password='admin2')

    def test_get_all_users(self):
        # get API response
        response = client.get(reverse('get'))
        # get data from db
        users = user.objects.all()
        serializer = userSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetAllProductsTest(TestCase):
    """ Test module for GET all puppies API """

    def setUp(self):
        product.objects.create(
            product_name='Jon Snow', product_model='Game of Thrones', product_size=9,
            product_description="Done with the Night's Watch? Yeah, we are too. And so is Jon Snow! Sure enough, death is the only way to be released from the vows of the Watch, and since Jon really did die up there in Castle Black, he has reason enough to head back home to Winterfell now that he's been resurrected."
            , product_stock=50,product_price=12.99,warranty="2 years",seller="Amazon",image='https://images.fun.com/products/42884/1-1/pop-game-of-thrones-jon-snow.jpg')

    def test_get_all_products(self):
        # get API response
        response = client.get(reverse('get'))
        # get data from db
        products = product.objects.all()
        serializer = productSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

"""class GetSingleProductTest(TestCase):

    def setUp(self):
        self.casper = product.objects.create(
            name='Casper', age=3, breed='Bull Dog', color='Black')
        self.muffin = Puppy.objects.create(
            name='Muffin', age=1, breed='Gradane', color='Brown')
        self.rambo = Puppy.objects.create(
            name='Rambo', age=2, breed='Labrador', color='Black')
        self.ricky = Puppy.objects.create(
            name='Ricky', age=6, breed='Labrador', color='Brown')

    def test_get_valid_single_puppy(self):
        response = client.get(
            reverse('get_delete_update_puppy', kwargs={'pk': self.rambo.pk}))
        puppy = Puppy.objects.get(pk=self.rambo.pk)
        serializer = PuppySerializer(puppy)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_puppy(self):
        response = client.get(
            reverse('get_delete_update_puppy', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)"""