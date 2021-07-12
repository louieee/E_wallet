from django.contrib import auth
from django.shortcuts import render, redirect

# Create your views here.
from Account.models import User
from E_Wallet.utilities import display
from Wallet.models import Transaction, Wallet


def deposit(request):
    context = dict()
    if request.method == 'GET':
        display_ = display(request)
        if display_ is not None:
            context = display_
        return render(request, 'Wallet/deposit.html', context=context)
    if request.method == 'POST':
        pass


def transfer(request):
    return render(request, 'Wallet/transfer.html')


def withdraw(request):
    return render(request, 'Wallet/withdraw.html')


def transactions(request):
    context = dict()
    type_ = request.GET['type']
    context['type'] = type_
    context['bank'] = False
    if type_ == 'withdrawal' or type_ == 'deposit':
        context['bank'] = True
    wallet = Wallet.objects.filter(user_id=request.user.id).first()
    if wallet is None:
        auth.logout(request)
        return redirect('login')
    if type_ == 'withdrawal':
        context['transactions'] = wallet.withdrawal_transactions()
    elif type_ == 'deposit':
        context['transactions'] = wallet.deposit_transactions()
    elif type_ == 'in_transfer':
        context['transactions'] = wallet.received_transfers()
    else:
        context['transactions'] = wallet.transfer_transactions()

    return render(request, 'Wallet/transactions.html', context=context)


def beneficiaries(request):
    if request.method == 'GET':
        beneficiaries_ = Wallet.objects.get(user_id=request.user.id).beneficiaries.all()
        return render(request, 'Wallet/beneficiaries.html', context={"beneficiaries": beneficiaries_})


def cards(request):
    if request.method == 'GET':
        cards_ = User.objects.get(id=request.user.id).cards()
        return render(request, 'Wallet/cards.html', context={"cards": cards_})


def add_beneficiary(request):
    return render(request, 'Wallet/add_beneficiary.html')


def add_card(request):
    return render(request, 'Wallet/add_card.html')
