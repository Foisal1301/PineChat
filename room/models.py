from django.contrib.auth.models import User
from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=255,blank=False)
    owner = models.ForeignKey(User,related_name="room_owner",blank=False,null=False,on_delete=models.CASCADE)
    password = models.CharField(max_length=255)
    members = models.ManyToManyField(User,blank=True)
    uuid = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(Room,related_name="messages",on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name="messages",on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    date_added = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    class Meta:
        ordering = ('date_added',)

    def __str__(self):
        return f"Message of {self.room} by {self.user}"

class Invite(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    sender = models.ForeignKey(User,related_name="invitor",on_delete=models.CASCADE)
    reciever = models.ForeignKey(User,related_name="guest",on_delete=models.CASCADE)

    def _str_(self):
        return f"{self.reciever} is invited by {self.sender} in {self.room}"