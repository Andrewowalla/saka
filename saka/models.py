from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from cloudinary.models import CloudinaryField
from django.forms import IntegerField

# Create your models here.
class HouseRental(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=60)
    admin = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name='hood')
    logo = CloudinaryField("image")
    description = models.TextField()
    health_no = models.IntegerField(null=True, blank=True)
    police_no = models.IntegerField(null=True, blank=True)
    no_houses = models.IntegerField(null=True)
    no_vacant_houses = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.name} hood'

    def create_houserental(self):
        self.save()

    def delete_houserental(self):
        self.delete()

    @classmethod
    def find_houserental(cls, houserental_id):
        return cls.objects.filter(id=houserental_id)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=80, blank=True)
    bio = models.TextField(max_length=254, blank=True)
    profile_picture = CloudinaryField("image")
    location = models.CharField(max_length=50, blank=True, null=True)
    houserental = models.ForeignKey(HouseRental, on_delete=models.SET_NULL, null=True, related_name='members', blank=True)

    def __str__(self):
        return f'{self.user.username} profile'   

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Business(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=254)
    description = models.TextField(blank=True)
    houserental = models.ForeignKey(HouseRental, on_delete=models.CASCADE, related_name='business')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owner')

    def __str__(self):
        return f'{self.name} business'

    def create_business(self):
        self.save()

    def delete_business(self):
        self.delete()  
    @classmethod
    def search_business(cls, name):
        return cls.objects.filter(name__icontains=name).all()

class Post(models.Model):
    title = models.CharField(max_length=120, null=True)
    post = models.TextField()
    unittype = models.CharField(max_length=120, blank=True)
    rentalunit = models.IntegerField(blank=True, null=True)
    bedrooms = models.IntegerField(blank=True, null=True)
    utilities = models.CharField(max_length=120, blank=True)
    monthlyrent = models.IntegerField(blank=True, null=True)
    caretakercontact = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='post_owner')
    hood = models.ForeignKey(HouseRental, on_delete=models.CASCADE, related_name='hood_post')
