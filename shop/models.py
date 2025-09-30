import datetime
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((True, "Listed"), (False, "Unlisted"))

# Create your models here.

class Product(models.Model):
    """
    Stores a single product's information.
    """
    CATEGORY_CHOICES = [
    
        (
            'Melee Weapons', 
            (
                ('onehanded', 'One-Handed Melee'),
                ('twohanded', 'Two-Handed Melee'),
            ),
        ),
        (
            'Ranged Weapons', 
        (
                ('bow', 'Bow'),
                ('crossbow', 'Crossbow'),
                ('exotic', 'Exotic'),
            ),
        ),
        (
            'Armor', 
            (
                ('light', 'Light Armor'),
                ('medium', 'Medium Armor'),
                ('heavy', 'Heavy Armor'),
            ),
        ),
        ('unknown', 'Unknown'),
    ]

    status = models.BooleanField(default=False)
    product_name = models.CharField(max_length=200, default="newProduct")
    subtitle = models.CharField(max_length=200, default="newProductDesc")
    category = models.CharField(max_length=109,
                  choices=CATEGORY_CHOICES,
                  default="unknown")
    main_image = CloudinaryField('image', default='placeholder')
    price = models.DecimalField(max_digits=7, decimal_places=2)
    stock_quantity = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    description = models.TextField()
    review_average = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"{self.product_name}"


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
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviewer")
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    review_score = models.IntegerField()

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"{self.product_id} Review: '{self.title}' submitted by {self.username}"