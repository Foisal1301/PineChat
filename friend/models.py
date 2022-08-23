from django.db import models
from django.contrib.auth.models import User

class MessageWithFriend(models.Model):
    sender = models.ForeignKey(User,related_name="sender",on_delete=models.CASCADE)
    receiver = models.ForeignKey(User,related_name="receiver",on_delete=models.CASCADE)
    message = models.TextField(blank=False)
    date_added = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    class Meta:
        ordering = ('date_added',)

    def __str__(self):
        return f"{self.sender} to {self.receiver}"

class FriendRequest(models.Model):
    sender = models.ForeignKey(User,related_name="req_sender",on_delete=models.CASCADE)
    receiver = models.ForeignKey(User,related_name="req_reciever",on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.sender} sends {self.receiver}"