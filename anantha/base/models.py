from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10, unique=True)  # For storing phone number
    post = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return self.user.first_name
    
class Dress(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    img = models.ImageField(null=True,blank=True,upload_to="images/")
    ds = models.TextField(max_length=2000)
    cat = models.CharField(max_length=20,null=True)
    def __str__(self):
        return self.name
    
class MyCart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    items = models.ManyToManyField(Dress)


    def __str__(self):
        return f"Cart of {self.user.username}"