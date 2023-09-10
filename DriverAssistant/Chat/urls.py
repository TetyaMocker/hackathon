from django.urls import path
from . import views


urlpatterns = [
    path('', views.chat_generator, name='chat'),
    path('message', views.add_message, name='message'),
    path('record', views.record_view, name='record'),
    path('update_flag', views.update_flag, name='update_flag')
]
