from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('messages/', views.message_list, name='message_list'),
    path('add_message/', views.add_message, name='add_message'),
    path('not_authorized/', views.not_authorized, name='not_authorized'),
]
