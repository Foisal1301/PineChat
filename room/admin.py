from django.contrib import admin

from .models import Room,Message,Invite

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Invite)