from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save 
import uuid

class User(AbstractUser):
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=150, unique=False)
    password = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, unique=True, blank=True)  # Change to CharField for phone

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        email_username, _ = self.email.split('@')
        if not self.fullname:
            self.fullname = email_username

        if not self.username:
            self.username = email_username

        super(User, self).save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to='image', default="default/default-user.jpg", null=True, blank=True)
    fullname = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    about = models.TextField(null=True, blank=True)
    pid = models.UUIDField(unique=True, default=uuid.uuid4, max_length=400)

    def __str__(self):
        return self.fullname or self.user.fullname

    def save(self, *args, **kwargs):
        if not self.fullname:
            self.fullname = self.user.email

        super(Profile, self).save(*args, **kwargs)
    
    def Create_user_profile(sender,instance,created,**kwargs):
        if created:
            Profile.objects.create(user=instance)

    def save_user_profile(sender,instance,**kwargs):
        instance.profile.save()

    post_save.connect(Create_user_profile,sender=user)
    post_save.connect(save_user_profile,sender=user)
    