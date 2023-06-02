from django.db import models
from django.contrib.auth.models import User
import filetype,os
from django.conf import settings

class MessageWithFriend(models.Model):
    sender = models.ForeignKey(User,related_name="sender",on_delete=models.CASCADE)
    receiver = models.ForeignKey(User,related_name="receiver",on_delete=models.CASCADE)
    message = models.TextField(blank=False)
    date_added = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    file = models.FileField(default=None,null=True,blank=True,upload_to='images/messagewithfriend')

    class Meta:
        ordering = ('date_added',)

    @property
    def is_file(self):
        if self.file.name:
            filename = self.file.name[25:]
            if filetype.is_image(str(settings.BASE_DIR)+self.file.url):
                return {'ftype':'image','filename':filename,'url':self.file.url}
            elif filetype.is_video(str(settings.BASE_DIR)+self.file.url):
                return {'ftype':'video','filename':filename,'url':self.file.url}
            elif filetype.is_audio(str(settings.BASE_DIR)+self.file.url):
                return {'ftype':'audio','filename':filename,'url':self.file.url}
            return {'ftype':'unknown','filename':filename,'url':self.file.url}
        return {'ftype':None}

    def delete(self,*args, **kwargs):
        if self.is_file['ftype'] != None:
            os.remove(str(settings.BASE_DIR)+self.file.url)
        super(MessageWithFriend,self).delete(*args,**kwargs)

    def __str__(self):
        return f"{self.sender} to {self.receiver}"

class FriendRequest(models.Model):
    sender = models.ForeignKey(User,related_name="req_sender",on_delete=models.CASCADE)
    receiver = models.ForeignKey(User,related_name="req_reciever",on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.sender} sends {self.receiver}"