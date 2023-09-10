from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rzd/', include('Authorization.urls')),
    path('rzd/chat/', include('Chat.urls'))
]
