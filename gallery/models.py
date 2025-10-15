from django.db import models
from django.contrib.auth.models import User
# from cloudinary.models import CloudinaryField

STATUS = ((True, "Listed"), (False, "Unlisted"))

# Create your models here.

class Art(models.Model):
    title = models.CharField(max_length=200, default="newProduct")
    subtitle = models.CharField(max_length=200, default="newProductDesc")