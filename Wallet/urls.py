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
from .views import deposit, withdraw, transactions, cards, \
    beneficiaries, transfer, add_beneficiary, add_card, delete_card, \
    delete_beneficiary, get_account_balance, get_beneficiary, get_source, get_card
urlpatterns = [
    path('deposit/', deposit, name="deposit"),
    path('withdraw/', withdraw, name="withdraw"),
    path('transfer/', transfer, name="transfer"),
    path('transactions/', transactions, name="transactions"),
    path('account_balance/', get_account_balance, name="account_balance"),
    path('cards/', cards, name="cards"),
    path('add_card/', add_card, name="add_card"),
    path('get_card/',get_card, name="get_card" ),
    path('delete_card/', delete_card, name="delete_card"),
    path('beneficiaries/', beneficiaries, name="beneficiaries"),
    path('add_beneficiary/', add_beneficiary, name="add_beneficiary"),
    path('delete_beneficiary/', delete_beneficiary, name="delete_beneficiary"),
    path('get_beneficiary/', get_beneficiary, name="get_beneficiary"),
    path('get_source/', get_source, name='get_source')

]
