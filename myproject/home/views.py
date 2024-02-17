from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.
def home(request):
    print("home실행")
    print(request.user.is_authenticated)
    print(request.user.username)
    return render(request, 'home/home.html')

##### 닉네임 변경
# 접속 화면
def nickname(request):
    return render(request, 'home/nickname.html')

# 변경하기
@login_required
def nickname_check(request):
    print("nickname_check실행")
    try:
        if request.method == 'POST':
            nickname_want = request.POST.get('nickname_want')
            user = request.user
            user.username = nickname_want
            user.save()
            response_data = {'message': 'Username이 업데이트되었습니다.'}
        else:
            response_data = {'message': '요청 형식에 문제가 발생했습니다.'}
    except:
        response_data = {'message': '중복된 닉네임입니다. 다른 닉네임을 이용해주세요'}
    return JsonResponse(response_data)