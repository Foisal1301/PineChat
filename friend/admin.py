from django.contrib import admin
from .models import MessageWithFriend,FriendRequest

admin.site.register(MessageWithFriend)
admin.site.register(FriendRequest)
