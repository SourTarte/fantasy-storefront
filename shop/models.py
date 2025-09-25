from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class Category(models.Model):
    name = models.CharField()


class Product(models.Model):
    """
    Stores a single product's information.
    """
    product_name = models.CharField(max_length=200)
    category_ID = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=0, related_name="product")
    price = models.DecimalField(max_digits=7, decimal_places=2)
    stock_quantity = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return f"Product name: {self.product_name} is {self.price}"


class Customer(models.Model):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    first_name = models.CharField()
    surname = models.CharField()
    is_active_user = models.BooleanField(default=True)

    def __str__(self):
        return f"Customer's username is {self.username}"


class Cart(models.Model):
    total_price = models.DecimalField(max_digits=7, decimal_places=2)


class Cart_Item(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stagedproduct")
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart")
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)


class Review(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="review")
    username = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="reviewer")
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    review_score = models.IntegerField()

    def __str__(self):
        return f"Review titled '{self.title}' written by {self.username}"