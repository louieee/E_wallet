from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login')


def login(request):
    return render(request, 'Account/login.html')


def signup(request):
    return render(request, 'Account/signup.html')


def dashboard(request):
    return render(request, 'Account/dashboard.html')


@login_required(login_url='login')
def update_image(request):
    if request.method == 'POST':
        image_ = request.FILES.get('user_img')
        request.user.profile_picture = image_
        request.user.save()
        return redirect('dashboard')


def edit_profile(request):
    return render(request, 'Account/edit_profile.html')


def logout(request):
    auth.logout(request)
    return redirect('home')


def forgot_password(request):
    if request.method == 'GET':
        return render(request, 'Account/forgot_password.html')
    else:
        return redirect('verify')


def enter_key(request):
    context = {"title": "Enter Key"}
    return render(request, 'Account/enter_key.html', context=context)


def update_email(request):
    return redirect('edit_profile')


def change_password(request):
    return redirect('edit_profile')