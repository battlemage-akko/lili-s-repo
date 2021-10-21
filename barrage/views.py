from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from barrage.models import test as barrageDatabase
from django.http import HttpResponse, JsonResponse

# Create your views here.
def video(request):

    return render(request,'video.html')

@csrf_exempt
def loadbarrage(request):
    barrage = []
    result = barrageDatabase.objects.all().order_by('b_time').values()
    for i in result:
        barrage.append(i)
    return JsonResponse(barrage, safe=False)
