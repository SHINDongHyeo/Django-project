from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def index(request):
    print("@!#!@#@!#@!")
    return render(request, 'point/index.html')

##### 포인트
# 포인트 얻기
def point_gain(request):
    user = request.user
    user.point += 10
    user.save()
    return render(request, 'point/index.html')

# 포인트 잃기
def point_lose(request):
    user = request.user
    user.point -= 10
    user.save()
    return render(request, 'point/index.html')

def roulette(request):
    return render(request, 'point/roulette.html')

def rouletteBat(request):
    return render(request, 'point/rouletteBat.html')

def hardRoulette(request):
    return render(request, 'point/hardRoulette.html')

def hardRouletteBat(request):
    return render(request, 'point/hardRouletteBat.html')

def save(request):
    point = int(request.POST.get("point"))
    print(point)
    user = request.user
    user.point += point
    user.save()
    data = {
        'renewPoint': user.point,
    }
    return JsonResponse(data)