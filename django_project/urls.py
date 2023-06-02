from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
	path("",include("core.urls")),
	path("rooms/",include("room.urls")),
	path("friends/",include("friend.urls")),
    path("accounts/",include("allauth.urls"))#allauth
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

admin.site.header = "Pinechat Administration"
admin.site.site_title = "Pinechat Administration"
admin.site.index_title = "Pinechat Administration"
admin.site.site_header = "Pinechat Administration"

handler404='core.views.handle404'
handler500='core.views.handle500'