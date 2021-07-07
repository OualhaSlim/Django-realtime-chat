# -*- coding: utf-8 -*-
from aylienapiclient import textapi
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.shortcuts import render
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from chatserver.functions import publish_message

client = textapi.Client("dba25e52", "a1616b9977c35e4f2ab92c4fb6ea4bb7")


def index(request):
    return render(request,'index.html')
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('index'))
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request,'registration.html',
                          {'user_form':user_form,
                           'registered':registered})
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse_lazy('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            failed_login = True
            return render(request,'login.html',
                          {'failed_login':failed_login})
    else:
        failed_login = False
        return render(request, 'login.html', {'failed_login':failed_login})

class BroadcastChatView(TemplateView):
    template_name = 'group_chat.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        # create a welcome message to be sent to everybody
        publish_message(user=request.user, message='Hello everybody',humor='')
        return super(BroadcastChatView, self).get(request, *args, **kwargs)

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(BroadcastChatView, self).dispatch(*args, **kwargs)
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        message = request.POST.get('message')
        sentiment = client.Sentiment({'text': message})
        if sentiment['polarity'] == "positive":
            humor = ':)'
        elif sentiment['polarity'] == "negative":
            humor = ':('
        else:
            humor = ':|'
        publish_message(user=request.user, message=message,humor=humor)
        return HttpResponse('OK')


def handler404(request):
    return HttpResponseRedirect(reverse_lazy('index'))
