from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
# from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('messages/', views.message_list, name='message_list'),
    path('add_message/', views.add_message, name='add_message'),
    path('not_authorized/', views.not_authorized, name='not_authorized'),
]
