from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.contrib.auth.models import auth
from django.contrib.auth import get_user_model
from django.conf import settings
from .auth_mailer import MicroApiMailer
from .models import User
from user_dashboard.models import Project
from django.contrib.auth.views import logout_then_login
from django.core.exceptions import ValidationError, ObjectDoesNotExist

import os
import requests
import json
import uuid




def signin(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    else:
        
        if request.method == 'POST':


            email = request.POST.get('email')
            password = request.POST.get('password')
            
            try:
                user = auth.authenticate(email=email, password=password)
                
                if user is not None:
                    auth.login(request, user)
                    name = user.last_project
                    if name:
                        project = Project.objects.filter(
                            user=user).get(last_project=True)
                    else:
                        project = Project.objects.create(
                            name="Default Project", user=user, token=uuid.uuid4().hex, last_project=True)
                        project.save()
                    return redirect("user_dashboard:dashboardu")
                else:
                    messages.info(request, 'Invalid credentials')
                    return redirect("accounts:signin")

            except ValidationError:
                messages.error(request, 'Unable to reach auth server')
                return redirect("accounts:signin")

    return render(request, "accounts/sign_in.html")


def signup(request):

    if request.user.is_authenticated:
        return redirect('index')
    else:

        if request.method == 'POST':
        
            username = request.POST['username']
            password = request.POST['pwd']
            confirmpwd = request.POST['confirmpwd']
            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            email = request.POST['email']
            
            if password == confirmpwd:
                try:
                    user = User.objects.get(email=email)
                    messages.info(request, 'Email is already taken')
                    return redirect('accounts:signup')
                    
                except User.DoesNotExist:
                    user = User.objects.create_user(email, username=username, first_name=first_name, last_name=last_name, password=password)
                    name = user.last_project
                    print(name)
                    if name:
                        project = Project.objects.filter(
                            user=user).get(last_project=True)
                    else:
                        project = Project.objects.create(
                            name="Default Project", user=user, token=uuid.uuid4().hex, last_project=True)
                        project.save()
                    user.last_project = project.name
                    user.save()
                    auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('accounts:signin')
            elif password == "":
                messages.error(request, 'Password field must be filled')
                return redirect('accounts:signup')
            else:
                messages.error(request, 'Password must match')
                return redirect('accounts:signup')


    return render(request, "accounts/sign_up.html")


def signout(request):
    return logout_then_login(request)
