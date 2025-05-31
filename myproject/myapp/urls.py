from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),

    # 🔐 Aktivace účtu
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('messages/', views.message_list, name='message_list'),
    path('add_message/', views.add_message, name='add_message'),
    path('not_authorized/', views.not_authorized, name='not_authorized'),

    # 🔐 Autentizace
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # 🔐 Reset hesla
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # 🔐 Změna hesla
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('cookies/', views.cookies_info, name='cookies_info'),

]
