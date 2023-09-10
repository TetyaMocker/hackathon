from django.urls import path
from . import views

urlpatterns = [
    path('authorization/', views.authorization, name='authorization')

]
