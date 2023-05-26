from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django import forms
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required


@user_passes_test(lambda u: u.is_superuser)
def user_list(request):
    users = User.objects.exclude(pk=request.user.pk)
    for user in users:
        user.has_orders = user.order_set.exists()
    context = {'users': users}
    return render(request, 'list_users.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_detail(request, pk):
    user = User.objects.get(pk=pk)
    context = {'user': user}
    return render(request, 'detail_user.html', context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                return redirect('user_list')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if not user:
        messages.error(request, 'User does not exist.')
        return redirect('user_list')

    has_orders = user.order_set.exists()
    if has_orders:
        return redirect('user_list')

    user.delete()
    messages.success(request, 'User deleted.')
    return redirect('user_list')


def home_view(request):
    return render(request, 'home.html')


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)
