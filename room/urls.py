from django.urls import path
from . import views

urlpatterns = [
    path("",views.rooms,name="rooms"),
    path("room/<str:pk>/",views.room,name="room"),
    path("room/<str:pk>/delete_room/",views.delete_room,name="delete-room"),
    path("room/<str:pk>/leave_room/<int:userid>",views.leave_room,name="leave-room"),
    path("room/<str:pk>/edit_room",views.edit_room,name="edit-room"),
    path("create_room/",views.create_room,name="create-room"),
    path("join_room/",views.join_room,name="join-room"),
    path("room/<str:pk>/invite/",views.invite,name="invite"),
    path("invitations/",views.invitations,name="invitations"),
    path("invitations/<int:pk>/accept/",views.accept_invite,name="accept-invite"),
    path("invitations/<int:pk>/decline/",views.decline_invite,name="decline-invite"),
    path("delete_message/<int:pk>/",views.delete_message,name="delete-message"),
    path("forward_message/<str:roomid>/<int:messageid>/",views.forward_message,name="forward-message"),
]
