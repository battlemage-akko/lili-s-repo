import json
from django.contrib.auth import authenticate ,login, logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import render,redirect
from django.http import HttpResponse
from app.models import AppUser as Userdatabase
from django.views.decorators.csrf import csrf_exempt
from myproject import urls

def test(request):
    return render(request,'test.html')
def index(request):
    return render(request,'index.html')
def login(request):
    return render(request,'login.html')
def wrapper(request):
    return render(request,'wrapper.html')

@csrf_exempt
def login_check(request):
    if (request.method == 'GET'):
        pass
    if(request.method == 'POST'):
        context = {
            'message': ''
        }
        username = request.POST.get("sign_in_Username")
        password = request.POST.get("sign_in_Password")
        print(password)
        thisuser = authenticate(username=username,password=password)
        print(thisuser)
        try:
            if thisuser:
                return redirect("index")
        except AttributeError:
            return HttpResponse("出错了")

        return HttpResponse("done")
# Create your views here.
