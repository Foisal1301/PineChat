from django.db import models

from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(null=True,blank=True,upload_to='images/profile_pic')
    verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=200,blank=True)
    friends = models.ManyToManyField(User,related_name="friends")
    activation_pass = models.CharField(max_length=1000,blank=True)

    def __str__(self):
        return f"Profile of {self.user}"