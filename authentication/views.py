# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect
from django.contrib import auth
from .forms import CustomUserCreationForm
from django.urls import reverse


def login(request):
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            request.session['login_error'] = 'Login and/or password are incorrect'
    return HttpResponseRedirect(reverse('landing'))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('landing'))


def register(request):
    context = dict()
    context['form'] = CustomUserCreationForm()
    if request.POST:
        new_user_form = CustomUserCreationForm(request.POST)
        context['form'] = new_user_form
        print(new_user_form)
        if new_user_form.is_valid():
            user = new_user_form.save()
            print(user)
            new_user = auth.authenticate(username=new_user_form.cleaned_data['username'],
                                         password=new_user_form.cleaned_data['password2'])
            auth.login(request, new_user)
            return HttpResponseRedirect(reverse('landing'))
        else:
            context['form'] = new_user_form
    return render(request, 'landing/main.html', context)
