"""E_Wallet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from .views import home, dashboard, login, signup, update_image, edit_profile, logout, forgot_password, enter_key
urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name="dashboard"),
    path('login/', login, name="login"),
    path('signup/', signup, name="signup"),
    path('update_image/', update_image, name='update_image'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('forgot_password/', forgot_password, name="forgot_password"),
    path('verify/', enter_key, name='verify'),
    path('logout/', logout, name="logout")
]
