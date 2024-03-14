from django.db import models
from django.contrib.auth.models import AbstractUser
from shortuuid.django_fields import ShortUUIDField

class User(AbstractUser):
    username = models.CharField(max_length=100)
    email= models.EmailField(max_length=254)
    password = models.CharField(max_length=100, blank=True) 
    phone = models.IntegerField( unique=True,blank=True)

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
       email_username,mobile=self.email.split('@')
       if self.fullname == '' :
           self.fullname== email_username

       if self.username == '' :
           self.username== email_username
          
       super(User, self).save(*args, **kwargs) # Call the real save() method
    

class Profile(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.FileField(upload_to='image',default="default/default-user.jpg",null=True,blank=True)
    fullname = models.CharField(max_length=100,null=True,blank=True)
    Gender = models.CharField(max_length=100,null=True,blank=True)
    Address = models.CharField(max_length=100,null=True,blank=True)
    Country = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    Date = models.DateField(auto_now_add=True)
    about=models.TextField(null=True,blank=True)
    pid=ShortUUIDField(unique=True,length=200 ,max_length=400,alphabet="abcdefghijk")    

    def __str__(self):
        if self.fullname:
            return str(self.fullname)
        else:
            return str(self.user.fullname)
        
    def save(self, *args, **kwargs):
       if self.fullname == '' :
           self.fullname== self.user.fullname
          
       super(Profile, self).save(*args, **kwargs) 