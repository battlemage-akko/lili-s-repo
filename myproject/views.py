from django.http import HttpResponse
from django.shortcuts import render


def test(request):
    return render(request,'test.html')
def index(request):
    return render(request,'index.html')
def login(request):
    return render(request,'login.html')
def wrapper(request):
    return render(request,'wrapper.html')

