from django.shortcuts import render

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