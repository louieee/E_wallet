from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


# Create your views here.


def home(request):
    return render(request, 'Account/home.html')


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
    return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('home')
