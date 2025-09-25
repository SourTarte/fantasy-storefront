from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from .models import Product

class TestBlogViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="myUsername",
            password="myPassword",
            email="test@test.com"
        )
        self.product = Product(product_name="Big Sword", price=2.50,
                         stock_quantity=3,description="Very big sword, very good for slashing. I killed a rock with this once.")
        self.product.save()

    def testProductOutput(self):
        response = self.client.get(reverse(
            'description', args=['product_name']))
        print(response)