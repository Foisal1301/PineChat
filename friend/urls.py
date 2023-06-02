from django.urls import path
from . import views

urlpatterns = [
    path("",views.friends,name="friends"),
    path("<int:pk>/",views.friend,name="friend"),
    path("friend_ajax/<int:pk>/",views.friend_ajax,name="friend-ajax"),
    path("delete_message/<int:pk>/",views.delete_message_frnd,name="delete-message-frnd"),
    path("forward_message/<int:userid>/<int:messageid>/",views.forward_message_frnd,name="forward-message-frnd"),
    path("unfriend/<int:pk>/",views.unfriend,name="unfriend"),
    path("friend_requests/",views.frnd_reqs,name="friend-requests"),
    path('add_friend/<int:pk>/',views.add_friend,name="add-friend"),
    path('accept_frendreq/<int:pk>',views.accept_frndreq,name="accept-friendreq"),
    path('decline_frendreq/<int:pk>',views.decline_frndreq,name="decline-friendreq"),
    path('search/',views.search,name="search"),
    path('search_ajax/',views.search_ajax,name="search_ajax"),
    path('cancel_friendreq/<int:pk>',views.cancel_friendreq,name="cancel-friendreq"),
    path('upload_files/<int:pk>/',views.uploadFile,name='uploadFile'),
]
