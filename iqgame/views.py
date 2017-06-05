# -*- coding: utf-8 -*-
from django.contrib import auth
from django.shortcuts import render
from authentication.forms import CustomUserCreationForm


def start_view(request):
    context = dict()
    error_message = request.session.get('login_error')
    if error_message:
        context['login_error'] = error_message
    context['username'] = auth.get_user(request).username
    context['form'] = CustomUserCreationForm()
    return render(request, 'landing/main.html', context)

