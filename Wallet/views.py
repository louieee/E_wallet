from django.shortcuts import render


# Create your views here.


def deposit(request):
    return render(request, 'Wallet/deposit.html')


def transfer(request):
    return render(request, 'Wallet/transfer.html')


def pay_bills(request):
    return render(request, 'Wallet/pay_bills.html')


def withdraw(request):
    return render(request, 'Wallet/withdraw.html')


def transactions(request):
    return render(request, 'Wallet/transactions.html')


def beneficiaries(request):
    return render(request, 'Wallet/beneficiaries.html')


def cards(request):
    return render(request, 'Wallet/cards.html')

