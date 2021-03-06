from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from app.models import setting as settingTable
from django.contrib.auth import get_user_model
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
User = get_user_model()

@login_required
def setting(request):
    return render(request,"setting.html")

@login_required
def setting_profile(request):
    return render(request,'setting_profile.html')

@login_required
def setting_avatar(request):
    return render(request,'setting_avatar.html')

@login_required
def setting_info(request):
    return render(request,'setting_info.html')

@login_required
def setting_password(request):
    return render(request,'setting_password.html')

@csrf_exempt
def password_check(request):
    if(request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('old_password')
        print(username,password)
        check_result = authenticate(username=username, password=password)
        if check_result:
            return JsonResponse({
                'code':1
            })
        else:
            return JsonResponse({
                'code': 0
            })
@csrf_exempt
def change_password(request):
    if(request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('new_password')
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        logout(request)
        return JsonResponse({
            "code":1
        })
@csrf_exempt
def getMySetting(request):
    if(request.method == 'POST'):
        u_id = request.POST.get('u_id')
        result = settingTable.getSettingById(u_id=u_id)
        data = {}
        for i in result.keys():
            if i != 'u_id':
                data[i] = 1 if result[i] else 0
        print(data)
        return JsonResponse(data)
@csrf_exempt
def changeMySetting(request):
    if (request.method == 'POST'):
        u_id = request.POST.get('u_id')
        option = request.POST.get('option')
        value = request.POST.get('value')
        settingTable.change(u_id=u_id,option=option,value=value)
    return HttpResponse()
