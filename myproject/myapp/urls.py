from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('messages/', views.message_list, name='message_list'),
    path('add_message/', views.add_message, name='add_message'),
]
