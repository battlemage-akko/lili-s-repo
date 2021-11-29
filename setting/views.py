from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.

@login_required
def setting(request):
    return render(request,"setting.html")

def setting_profile(request):
    return render(request,'setting_profile.html')

def setting_avatar(request):
    return render(request,'setting_avatar.html')