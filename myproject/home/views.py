from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from community.models import Post
from chat.models import ChatRoom
from django.db.models import Count
from home.models import CustomUser

# Create your views here.
def home(request):
    point_rankers = CustomUser.objects.order_by("-point")[:5]
    hot_posts = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count',"-timestamp")[:5]
    recent_posts = Post.objects.order_by("-timestamp")[:5]
    hot_chats = ChatRoom.objects.all()[:5]

    context = {
        'point_rankers':point_rankers,
        'hot_posts':hot_posts,
        'recent_posts':recent_posts,
        'hot_chats':hot_chats,
    }
    return render(request, 'home/home.html', context=context)

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

def mypage(request):
    user = request.user
    written_posts = user.written_posts.all()
    like_posts = user.like_users.all()
    written_comments = user.user_comment.all()
    context = {
        'written_posts':written_posts,
        'like_posts':like_posts,
        'written_comments':written_comments
    }
    return render(request, 'home/mypage.html', context=context)

def changeprofile(request):
    user = request.user
    print(request.method)
    user.profile = request.FILES['photo']
    user.save()
    
    return mypage(request)