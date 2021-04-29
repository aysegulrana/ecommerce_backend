import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import product
from ..serializers import productSerializer
from ..models import user
from ..serializers import userSerializer
"""from ..models import cart
from ..serializers import cartSerializer
from ..models import orders
from ..serializers import ordersSerializer"""


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

class CreateNewUserTest(TestCase):
    """ Test module for inserting a new puppy """

    def setUp(self):
        self.valid_payload = {
            'email': "admin2@admin.com",
            'firstname': "Team 6",
            'lastname': "Admin",
            'address': "Izmit",
            'password': "adminr123"
        }
        self.invalid_payload = {
            'email': "",
            'firstname': "Team 6",
            'lastname': "Admin",
            'address': "Istanbul",
            'password': "adminr123"
        }

    def test_create_valid_user(self):
        response = client.post(
            reverse('post'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):
        response =client.post(
            reverse('post'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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

class GetSingleProductTest(TestCase):

    def setUp(self):
        self.jon=  product.objects.create(
            product_name='Jon Snow', product_model='Game of Thrones', product_size=9,
            product_description="Done with the Night's Watch? Yeah, we are too. And so is Jon Snow! Sure enough, death is the only way to be released from the vows of the Watch, and since Jon really did die up there in Castle Black, he has reason enough to head back home to Winterfell now that he's been resurrected."
            , product_stock=50,product_price=12.99,warranty="2 years",seller="Amazon",image='https://images.fun.com/products/42884/1-1/pop-game-of-thrones-jon-snow.jpg')

        self.arya = product.objects.create(
        product_name='Arya Stark', product_model='Game of Thrones', product_size=9,
        product_description=" A Game of Weapons\r\nWell, there are a lot of really dangerous people in Westeros. But, we would argue, that none are as dangerous or lethal as Arya Stark. Arya has been training for years, training with the best. Even training with a variety of weapons. She is not someone to be trifled with."
        , product_stock=50, product_price=12.99, warranty="2 years", seller="Amazon",
        image='https://images-na.ssl-images-amazon.com/images/I/519EUkzDsZL._AC_SL1001_.jpg')

    def test_get_valid_single_product(self):
        response = product.get(
            reverse('get', kwargs={'pk': self.jon.id}))
        prod = product.objects.get(pk=self.jon.id)
        serializer = productSerializer(prod)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_product(self):
        response = product.get(
            reverse('get', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CreateNewProductTest(TestCase):
    """ Test module for inserting a new puppy """

    def setUp(self):
        self.valid_payload = {
            'product_name': "Arya Stark",
            'product_model': "Game of Thrones",
            'product_size': 9,
            'product_description': "A Game of Weapons\r\nWell, there are a lot of really dangerous people in Westeros. But, we would argue, that none are as dangerous or lethal as Arya Stark. Arya has been training for years, training with the best. Even training with a variety of weapons. She is not someone to be trifled with.",
            'product_stock': 50,
            'product_price': 12.99,
            'warranty': "2 years",
            'seller': "Amazon",
            'image': "https://images.fun.com/products/62353/1-1/-two-headed-spear.jpg"
        }
        self.invalid_payload = {
            'product_name': "",
            'product_model': "",
            'product_size': 3,
            'product_description': "Bran Power\r\nMissing your beloved Game of Thrones? Use your Funko collection and replay your favorite moments! You'll need this Pop! TV King Bran the Broken Figure, then. It's a lifelike replica of the new ruler. He may look a little stoic, but he's just tired—he's been through a lot to get here",
            'product_stock': 50,
            'product_price': 12.99,
            'warranty': "2 years",
            'seller': "Amazon",
            'image': "https://images.fun.com/products/62926/1-1/pop-tv-game-of-thrones-king-bran-the-broken.jpg"
        }

    def test_create_valid_product(self):
        response = client.post(
            reverse('post'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_product(self):
        response = client.post(
            reverse('post'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateSinglePuroductTest(TestCase):
    """ Test module for updating an existing puppy record """

    def setUp(self):
        self.jon = product.objects.create(
            product_name='Jon Snow', product_model='Game of Thrones', product_size=9,
            product_description="Done with the Night's Watch? Yeah, we are too. And so is Jon Snow! Sure enough, death is the only way to be released from the vows of the Watch, and since Jon really did die up there in Castle Black, he has reason enough to head back home to Winterfell now that he's been resurrected."
            , product_stock=50, product_price=12.99, warranty="2 years", seller="Amazon",
            image='https://images.fun.com/products/42884/1-1/pop-game-of-thrones-jon-snow.jpg')

        self.arya = product.objects.create(
            product_name='Arya Stark', product_model='Game of Thrones', product_size=9,
            product_description=" A Game of Weapons\r\nWell, there are a lot of really dangerous people in Westeros. But, we would argue, that none are as dangerous or lethal as Arya Stark. Arya has been training for years, training with the best. Even training with a variety of weapons. She is not someone to be trifled with."
            , product_stock=50, product_price=12.99, warranty="2 years", seller="Amazon",
            image='https://images-na.ssl-images-amazon.com/images/I/519EUkzDsZL._AC_SL1001_.jpg')
        self.valid_payload = {
            'product_name': "Arya Stark",
            'product_model': "Game of Thrones",
            'product_size': 9,
            'product_description': "A Game of Weapons\r\nWell, there are a lot of really dangerous people in Westeros. But, we would argue, that none are as dangerous or lethal as Arya Stark. Arya has been training for years, training with the best. Even training with a variety of weapons. She is not someone to be trifled with.",
            'product_stock': 50,
            'product_price': 12.99,
            'warranty': "2 years",
            'seller': "Amazon",
            'image': "https://images.fun.com/products/62353/1-1/-two-headed-spear.jpg"
        }
        self.invalid_payload = {
            'product_name': "",
            'product_model': "",
            'product_size': 3,
            'product_description': "Bran Power\r\nMissing your beloved Game of Thrones? Use your Funko collection and replay your favorite moments! You'll need this Pop! TV King Bran the Broken Figure, then. It's a lifelike replica of the new ruler. He may look a little stoic, but he's just tired—he's been through a lot to get here",
            'product_stock': 50,
            'product_price': 12.99,
            'warranty': "2 years",
            'seller': "Amazon",
            'image': "https://images.fun.com/products/62926/1-1/pop-tv-game-of-thrones-king-bran-the-broken.jpg"

        }

    def test_valid_update_product(self):
        response = client.put(
            reverse('get', kwargs={'pk': self.arya.id,'x':1,'count':4}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_product(self):
        response = client.put(
            reverse('get', kwargs={'pk': self.arya.id,'x':1,'count':4}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeleteSingleProductTest(TestCase):
    """ Test module for deleting an existing puppy record """

    def setUp(self):
        self.jon = product.objects.create(
            product_name='Jon Snow', product_model='Game of Thrones', product_size=9,
            product_description="Done with the Night's Watch? Yeah, we are too. And so is Jon Snow! Sure enough, death is the only way to be released from the vows of the Watch, and since Jon really did die up there in Castle Black, he has reason enough to head back home to Winterfell now that he's been resurrected."
            , product_stock=50, product_price=12.99, warranty="2 years", seller="Amazon",
            image='https://images.fun.com/products/42884/1-1/pop-game-of-thrones-jon-snow.jpg')

        self.arya = product.objects.create(
            product_name='Arya Stark', product_model='Game of Thrones', product_size=9,
            product_description=" A Game of Weapons\r\nWell, there are a lot of really dangerous people in Westeros. But, we would argue, that none are as dangerous or lethal as Arya Stark. Arya has been training for years, training with the best. Even training with a variety of weapons. She is not someone to be trifled with."
            , product_stock=50, product_price=12.99, warranty="2 years", seller="Amazon",
            image='https://images-na.ssl-images-amazon.com/images/I/519EUkzDsZL._AC_SL1001_.jpg')

    def test_valid_delete_product(self):
        response = client.delete(
            reverse('get', kwargs={'pk': self.jon.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_product(self):
        response = client.delete(
            reverse('get', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)