"""Leket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from LeketIsraelApp import views
from LeketIsraelApp import forms
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetConfirmView
from LeketIsraelApp.forms import CustomSetPasswordForm


urlpatterns = [
    path('', include('LeketIsraelApp.urls')),
    path('admin/', admin.site.urls),
    path('signup', views.signup, name="signup"),
    path('login', views.custom_login, name="login"),
    path('logout', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('password_reset/',auth_views.PasswordResetView.as_view(form_class=forms.CustomPasswordResetForm),name="password_reset_form"),
    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    path('password_done',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(form_class=CustomSetPasswordForm), name='password_reset_confirm'),
]


