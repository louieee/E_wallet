from django.shortcuts import render


# Create your views here.


def deposit(request):
    return render(request, 'Wallet/deposit.html')


def transfer(request):
    return render(request, 'Wallet/transfer.html')


def withdraw(request):
    return render(request, 'Wallet/withdraw.html')


def transactions(request):
    type_ = request.GET['type']
    bank = False
    if type_ == 'withdrawal' or type_ == 'deposit':
        bank = True

    return render(request, 'Wallet/transactions.html', context={"type": type_, 'bank': bank})


def beneficiaries(request):
    return render(request, 'Wallet/beneficiaries.html')


def cards(request):
    return render(request, 'Wallet/cards.html')


def add_beneficiary(request):
    return render(request, 'Wallet/add_beneficiary.html')


def add_card(request):
    return render(request, 'Wallet/add_card.html')
