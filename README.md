# <img src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white"/> Django-project
## 🔎개요
장고를 활용한 웹 사이트를 제작 연습입니다.
http://agzg.hiitnative.com/
- 주제
  - 축구 커뮤니티⚽
- 기술셋
  - 백엔드 : <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white"/>, <img src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white"/>
  - 프론트엔드 : <img src="https://img.shields.io/badge/Bootstrap-7952B3?style=flat-square&logo=bootstrap&logoColor=white"/>, <img src="https://img.shields.io/badge/Javascript-F7DF1E?style=flat-square&logo=javascript&logoColor=white"/>

ex)
홈 화면

<img width="633" alt="스크린샷 2024-02-18 015529" src="https://github.com/SHINDongHyeo/Django-project/assets/96512568/4808a76d-22c6-447f-802c-2f05b0a910f6">



## 📃구현 기능 목록
- [장고 user 커스텀](#장고-user-커스텀)
- [소셜 로그인 기능](#소셜-로그인-기능)
- [게시물 기능](#게시물-기능)
- [API 활용 기능](#API-활용-기능)
- [쪽지 기능](#쪽지-기능)
- [실시간 채팅 기능(Channels)](#실시간-채팅-기능)
- [스케줄러를 통한 자동화(Celery)](#스케줄러를-통한-자동화)

## 장고 user 커스텀

- 설명

장고에서 기본적으로 제공하는 user에 내가 원하는 컬럼 추가하여 커스터마이징

- 구현 방법

AbstractUser를 상속받는 방식을 이용했습니다. 아래 코드는 point, level, notread, reported라는 추가 컬럼을 생성하는 예시입니다.

1. models.py 수정
```
# models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    point = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    notread = models.IntegerField(default=0)
    reported = models.IntegerField(default=0)
```

2. settings.py 수정

```
# settings.py

AUTH_USER_MODEL = '앱이름.CustomUser'
```


3. migrate 진행
```
python manage.py makemigrations
python manage.py migrate
```

## 소셜 로그인 기능

![image](https://github.com/SHINDongHyeo/Django-project/assets/96512568/1278aa0b-e188-47e9-a909-82f79fc45ee7)

- 설명

구글 계정을 이용한 로그인 기능 구현(회원가입은 따로 구현하지 않고 손쉽게 로그인할 수 있도록 구글 로그인만 구현)

- ERD

<img width="400" alt="image" src="https://github.com/SHINDongHyeo/Django-project/assets/96512568/d5582036-0611-44c5-9706-90f82aa776d0">

장고는 기본적으로 계정에 대한 모델을 제공합니다. 이것이 바로 user 모델입니다.(위 사진보다 더 많은 필드가 존재하지만 간단하게 몇 개의 필드만 표시함) 그리고 allauth는 이런 장고 기본 user 모델을 외래키로 받는 socialaccount 모델을 추가하는 형식을 취합니다. 즉, 소셜 로그인 진행 시 user 모델에 데이터가 생기고 이 모델을 참조하는 socialaccount 모델 데이터가 따라 생깁니다. 이는 allauth의 models.py 중 SocialAccount에 관한 코드를 통해 확인할 수 있습니다.

```
# 가상환경\Lib\site-packages\allauth\socialaccount\models.py

class SocialAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ...
```


- 구현 방법

장고에서는 `allauth`를 통해 손쉽게 소셜 로그인 구현이 가능합니다. 참조 문서 (https://docs.allauth.org/en/latest/installation/quickstart.html)

1. `allauth` 설치
```
pip install django-allauth
```

2. settings.py 수정
```
# Specify the context processors as follows:
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Already defined Django-related contexts here

                # `allauth` needs this from django
                'django.template.context_processors.request',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    ...
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
    ...
]

INSTALLED_APPS = [
    ...
    # The following apps are required:
    'django.contrib.auth',
    'django.contrib.messages',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    ...
]

MIDDLEWARE = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",

    # Add the account middleware:
    "allauth.account.middleware.AccountMiddleware",
)

# Provider specific settings 이 부분은 아래 내용 참고
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '123',
            'secret': '456',
            'key': ''
        }
    }
}
```
SOCIALACCOUNT_PROVIDERS 정보는 소셜 로그인 기능을 제공하는 기업에서 따로 받아서 넣어주는 것입니다. 예를 들어 구글 로그인 기능을 추가하기 위해서는 구글 계정에 접속하며 OAuth 제공자를 만들고 해당 제공자의 client_id, secret, key 등의 정보를 받아서 settings.py에 넣어줘야 합니다. 카카오, 네이버 등의 로그인 기능을 추가하기 위해서는 각 기업의 사이트에 맞는 OAuth 정보 추가가 필요합니다.(이 부분이 필요하시면 따로 검색)

3. urls.py 수정
```
urlpatterns = [
    ...
    path('accounts/', include('allauth.urls')),
    ...
]
```

4. migrate 진행
```
python manage.py migrate
```



## 게시물 기능

<img width="591" alt="image" src="https://github.com/SHINDongHyeo/Django-project/assets/96512568/90de5245-2740-49eb-8318-286fe58eb4e2">

<img width="467" alt="image" src="https://github.com/SHINDongHyeo/Django-project/assets/96512568/e210dcfa-f235-4b98-84f5-f946618f3563">


- 설명

일반적인 커뮤니티에 존재하는 게시물과 같이 유저가 게시물을 작성할 수 있고, 해당 게시물을 여러 유저가 '좋아요'를 눌러 추천할 수 있는 기능을 구현. 또한 게시물에 댓글을 달 수 있고 댓글은 댓글에 대한 댓글을 달 수 있도록 구현(깊이가 무한히 깊어질 수 있게)

- ERD

<img width="700" alt="image" src="https://github.com/SHINDongHyeo/Django-project/assets/96512568/ae398897-bf71-4d5a-90b4-ab898a778842">

유저는 여러 게시물을 작성할 수 있습니다. 하지만 여러 유저가 동시에 한 게시물을 작성할 수는 없습니다. 그러므로 유저와 게시물의 관계는 1:N 관계입니다.

하지만 유저는 여러 게시물을 좋아할 수 있고, 여러 유저가 동시에 한 게시물을 좋아할 수도 있습니다. 그러므로 게시물 좋아요와 유저의 관계는 N:M 관계입니다.

유저는 여러 댓글을 작성할 수 있습니다. 하지만 여러 유저가 동시에 한 댓글을 작성할 수는 없습니다. 그러므로 유저와 댓글의 관계는 1:N 관계입니다.

게시물은 여러 댓글을 포함할 수 있습니다. 하지만 여러 게시물이 동시에 한 댓글을 포함할 수는 없습니다. 그러므로 게시물과 댓글을 관계는 1:N 관계입니다.

- 구현 방법

1. models.py 수정


```
from django.db import models
from home.models import CustomUser
from tinymce.models import HTMLField

class Post(models.Model):
    type = models.IntegerField(default=0)
    likes = models.ManyToManyField(CustomUser, blank=True, related_name='like_users')
    author = models.ForeignKey(CustomUser, related_name='written_posts', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    content = HTMLField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='post_comments', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, related_name='user_comment', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self',null=True,blank=True, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

```

2. migrate 진행
```
python manage.py makemigrations
python manage.py migrate
```

3. views.py 수정



```
def post(request, id):
    post = Post.objects.filter(id=id).first()
    comments = Comment.objects.filter(post=id, parent_comment=None).order_by("timestamp") # parent_comment가 없는 댓글(최상위 댓글)들만 먼저 뽑아서 전달함
 
    context ={
        'post': post,
        'comments':comments
    }
    return render(request, 'community/post.html', context=context)
```

4. html 수정

댓글의 깊이를 표현하기 위해 재귀적으로 html 파일을 호출하는 방식 이용

```
# recomments.html

<!-- 대댓글 -->
<div class="ps-3">
{% for comment in comments %}
    <div class="p-3 card">{{ comment.content }}</div>
    <div class="ps-3">
    {% if comment.comment_set.all %}
        {% for sub_comment in comment.comment_set.all %}
            <div class="p-3 card">{{ sub_comment.content }}</div>
            {% include 'community/recomments.html' with comments=sub_comment.comment_set.all %}
        {% endfor %}
    {% endif %}
    </div>

{% endfor %}
</div>

```

댓글 깊이 별 div 마진 차이를 주어 쉽게 확인할 수 있도록 표현

```
# post.html

...

<div id="comments">
    <div class="fw-bold">댓글</div>
    {% for comment in comments %}
        <div class="p-3 card">{{ comment.content }}</div>
        {% include 'community/recomments.html' with comments=comment.comment_set.all %}
    {% endfor %}
</div>

```



## API 활용 기능

<img width="596" alt="image" src="https://github.com/SHINDongHyeo/Django-project/assets/96512568/723b10e5-34d6-48a3-948d-fe7e306f4bed">

- 설명

https://www.football-data.org/ 에서 제공하는 무료 API를 활용해 해외 축구 리그 정보를 불러와 사용


- 구현 방법

1. 위 링크에 가입하여 X-Auth-Token 데이터를 제공받습니다.
2. views.py에서 다음과 같은 형식의 코드를 통해 json 데이터를 호출합니다.

```
# views.py

import requests

json_data = requests.get("http://api.football-data.org/v4/competitions/PL/matches",
                         headers={
                             'X-Auth-Token': '자신의계정을통해확인',
                         }).json()
```
3. json 데이터 예시
```
{
    "filters": {
        "season": "2023"
    },
    "resultSet": {
        "count": 380,
        "first": "2023-08-11",
        "last": "2024-05-19",
        "played": 244
    },
    "competition": {
        "id": 2021,
        "name": "Premier League",
        "code": "PL",
        "type": "LEAGUE",
        "emblem": "https://crests.football-data.org/PL.png"
    },
    ...
```





## 쪽지 기능

<img width="594" alt="image" src="https://github.com/SHINDongHyeo/Django-project/assets/96512568/16ead48a-f4b6-4a9e-a212-ec7922f36166">



- 설명

유저 간 쪽지를 주고 받을 수 있는 쪽지(메일) 기능 구현

- ERD

<img width="400" alt="image" src="https://github.com/SHINDongHyeo/Django-project/assets/96512568/3cd0e742-bf66-47a0-b352-a0caccf69f90">

Mail과 Users는 다대일 관계(1:N)입니다. 하나의 유저는 여러 쪽지를 가질 수 있지만, 하나의 쪽지는 여러 보낸이나 여러 받는이를 가질 수 없습니다.






- 구현 방법

1. models.py 수정

(저는 user를 커스텀한 CustomUser를 사용 중이므로 아래와 같이 내가 커스텀한 CustomUser를 불러와 사용했습니다.)
```
# models.py

from django.db import models
from home.models import CustomUser

# Create your models here.
class Mail(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sent_mails', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_mails', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
```

2. migrate 진행
```
python manage.py makemigrations
python manage.py migrate
```

3. views.py 수정

```
# html에서 쪽지에 대한 form데이터 전송 받은 후
def mail_write_check(request): 
    if request.method == 'POST':
        user = request.user
        receiver = request.POST.get('receiver')
        subject = request.POST.get('subject')
        content = request.POST.get('content')
        print(receiver,subject,content)

        receiver_real = CustomUser.objects.filter(username=receiver).first() # 받는이가 실존하는지 체크
        if receiver_real is not None:
            mail = Mail.objects.create( # 쪽지 생성
                sender=user,
                receiver=receiver_real,
                subject = subject,
                content = content,
                )
            mail.save() # 쪽지 저장
            msg = {
                'status': "success",
                'msg' : "쪽지가 성공적으로 전송되었습니다"
                }
            return JsonResponse(msg) # html단에서 ajax를 통해 비동기 방식을 이용했으므로 json 데이터를 전송했습니다
        else:
            print("없는 계정")
            msg = {
                'status': "fail",
                'msg' : "받는 사람에 해당 하는 계정이 존재하지 않습니다"
                }
            return JsonResponse(msg)
```

## 실시간 채팅 기능

<img width="534" alt="image" src="https://github.com/SHINDongHyeo/Django-project/assets/96512568/996550d4-4016-4b7d-9710-d2b8ac0e0af1">


- 설명

웹 사이트에 접속한 유저 간 실시간 채팅을 할 수 있는 기능 구현(`Channels` 활용)

- ERD

<img width="400" alt="image" src="https://github.com/SHINDongHyeo/Django-project/assets/96512568/14bfeb36-5d2b-4ef5-9cde-fde7b8fb7f27">

채팅방과 유저는 일대일 관계(1:1)입니다. 채팅방의 주인은 단 한 명 존재할 수 있고, 유저 또한 단 하나의 채팅방만을 가질 수 있습니다.


- 구현 방법

1. models.py 수정

(저는 user를 커스텀한 CustomUser를 사용 중이므로 아래와 같이 내가 커스텀한 CustomUser를 불러와 사용했습니다.)
```
# models.py

from django.db import models
from home.models import CustomUser

class ChatRoom(models.Model):
    title = models.CharField(max_length=255)
    current = models.IntegerField(default=1)
    limit = models.IntegerField(default=2)
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
```

2. `Channels` 설치

`Channels`는 장고에서 제공되는 웹 소캣(WebSocket) 사용 라이브러리입니다. WebSocket은 클라이언트와 서버(브라우저와 서버)를 연결하고 실시간으로 통신이 가능하도록 하는 기술을 의미합니다.

```
python -m pip install -U 'channels[daphne]'
```

3. settings.py 수정

참조문서(https://channels.readthedocs.io/en/latest/installation.html)

```
# settings.py

INSTALLED_APPS = (
    "daphne",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    ...
)

ASGI_APPLICATION = "자신프로젝트명.asgi.application"


# 여러 명이 같은 웹 소캣에 동시 접속할 수 있도록 하는 설정(이는 개발 단계에서 확인용으로 넣은 설정. 배포 시에는 다르게 작성해야함)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

```

4. asgi.py 수정

```
# asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    )
})
```

5. routing.py 추가

```
from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<int:room_id>', ChatConsumer.as_asgi()),
]
```

6. consumers.py 추가

```
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        # 채팅방(Room) 이름을 URL 매개변수에서 가져와서 사용
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_id = f"chat_{self.room_id}"
        
        # 채팅방 그룹에 참여
        await self.channel_layer.group_add(
            self.room_group_id,
            self.channel_name
        )
    
        await self.accept()

    async def disconnect(self, close_code):
        # 채팅방 그룹에서 나가기
        await self.channel_layer.group_discard(
            self.room_group_id,
            self.channel_name
        )
        

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        type = text_data_json['type']

        # 채팅방 그룹에 메시지 브로드캐스트
        await self.channel_layer.group_send(
            self.room_group_id,
            {
                'type': 'chat.message',
                'message': message,
                'mytype': type
            }
        )

  # 채팅방 그룹으로부터 메시지 수신
    async def chat_message(self, event):
        message = event['message']
        type = event['mytype']

        # WebSocket으로 메시지 전송
        await self.send(text_data=json.dumps({
            'message': message,
            'type' : type
        }))

```



7. javascript 코드 작성

```
// 웹 소켓에 연결(routing.py에서 설정한 주소로 연결)
const socket = new WebSocket('ws://127.0.0.1:8000/ws/chat/{{ chatroom.id }}');

// 웹 소캣에 연결되었을 경우
socket.onopen = function() {
    console.log('WebSocket 연결이 열렸습니다.');
    var msg = "{{request.user.username }}님이 대화에 참여하셨습니다";
    const message = {
        'type': -1,
        'message': msg
    };
    socket.send(JSON.stringify(message)); 
};

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log('서버로부터 메시지를 받았습니다:', data.message);
    var type = data.type;
    var message = data.message;
    console.log(type);
    if (type == -1) {
        var newDiv = document.createElement("div");
        var newChat = document.createElement("div");
        newDiv.classList = "d-flex justify-content-center"
        newChat.classList = "border text-center"
        newChat.textContent = data.message;
        newDiv.append(newChat);
        chatLog.append(newDiv);
    }else if (type == {{ request.user.id }} ) {
        var newDiv = document.createElement("div");
        var newChat = document.createElement("div");
        newDiv.classList = "d-flex justify-content-end"
        newChat.classList = "d-inline-block rounded-2 bg-primary text-white border-bottom border-end"
        newChat.textContent = data.message;
        newDiv.append(newChat);
        chatLog.append(newDiv);
    }else {
        var newDiv = document.createElement("div");
        var newChat = document.createElement("div");
        newDiv.classList = "d-flex justify-content-start"
        newChat.classList = "d-inline-block rounded-3 bg-light text-dart border-bottom border-end"
        newChat.textContent = data.message;
        newDiv.append(newChat);
        chatLog.append(newDiv);
    };
    chatLog.scrollTop = chatLog.scrollHeight;
};

socket.onclose = function() {
    console.log('WebSocket 연결이 종료되었습니다.');
};

function send_msg(){
    var msg = $('#chat-message-input').val();
    const message = {
        'type': {{ request.user.id }},
        'message': msg
    };
    socket.send(JSON.stringify(message)); 
    chatInput.value = "";
};

```


## 스케줄러를 통한 자동화

- 설명

장고에서는 여러 스케줄러를 이용해 원하는 작업을 특정 시간마다 실행할 수 있도록 할 수 있습니다. 해당 스케줄러로는 다양한 것들이 존재합니다.

1. 셀러리(celery)
2. 

- 구현 방법 : 셀러리(celery)

1. 설치 

```
pip install 'celery[redis]'

pip install django_celery_beat

pip install django_celery_results


sudo apt-get install redis-server # 우분투 경우
```
윈도우의 경우 https://github.com/microsoftarchive/redis/releases 링크에서 msi 파일을 다운받아 직접 설치하면 됩니다.

설치 완료 후 redis 정상 작동을 확인하기 위해서는 터미널창에서 아래 명령어를 통해 확인합니다.

```
redis-server # redis-server 실행

redis-cli # redis-client 실행. 이후 ping이라고 타이핑해봄
ping
PONG # ping에 대한 대답으로 PONG이 출력되면 정상
```

2. myproject/__init__.py 수정

```
from .celery import app as celery_app

__all__ = ['celery_app']
```

3. myproject/celery.py 수정

```
from __future__ import absolute_import, unicode_literals
import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Require: {0!r}'.format(self.request))
```

4. myproject/settings.py 수정

```

INSTALLED_APPS = [
    ...

    'django_celery_beat',
    'django_celery_results',
]


CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Seoul'
CELERY_BEAT_SCHEDULE = {
    'task-number-one': {
        'task': 'home.tasks.celery_check',  # 실행하고 싶은 작업(home app 하위 tasks.py 파일 안 celery_check 함수 실행)
        'schedule':10.0,
    }
}
```

5. home/celery.py 수정

```
from celery import shared_task
from django.db import transaction

import logging

logger = logging.getLogger(__name__)

@shared_task()
def celery_check():
    with open("test.txt", "a")  as f:
        f.write("확인")

    logger.info("Starting to update congestion data.")
    
```


6. celery beat, worker 실행
beat는 작업 일정을 알려주고, worker는 작업 일정대로 일한다라고 생각하면 쉽습니다. 아래 명령어는 내 장고 프로젝트 최상단 경로에서 터미널창을 이용해 실행합니다.(앱 폴더들이 위치한 경로)

- celery beat

```
celery -A myproject beat -l info
```

저는 위에서 settings.py를 보시면 schedule(일 시킬 시간 주기)을 10.0초로 설정했습니다.

```
CELERY_BEAT_SCHEDULE = {
    'task-number-one': {
        'task': 'home.tasks.celery_check',  # 실행하고 싶은 작업(home app 하위 tasks.py 파일 안 celery_check 함수 실행)
        'schedule':10.0,
    }
}
```

그러므로 10초마다 결과물이 화면에 출력되는 모습을 확인할 수 있습니다. 하지만 해당 결과는 작업을 예정해 놓기만 한 것이고 실제로 실행한 것은 아니므로 실질적인 결과물은 아직 확인할 수 없습니다.

- celery worker


```
celery -A myproject worker -l info
```

위 명령어를 통해 실제 예정된 작업들이 수행되고 해당 결과도 확인할 수 있습니다. 저의 경우 실행되는 파일인 home앱 tasks.py 코드의 celery_check함수의 작업이 test.txt라는 파일을 열고 "확인"이라는 텍스트를 계속해서 추가하는 작업이었기 때문에 계속해서 "확인"이라는 문구가 적힌 test.txt 파일을 확인할 수 있습니다.

⚠️ 에러
여기서 만약 정상적으로 worker 실행이 되지 않는 경우가 있을 수 있습니다. 보통 윈도우에서 이런 경우가 많이 발생하고 이는 celery가 더 이상 윈도우에서 서비스를 지원하지 않기 때문입니다. 이를 위해서 아래와 같은 방법으로 간단하게 에러를 해결할 수도 있습니다. gevent 설치 후 해당 옵션을 사용하는 것입니다.

```
pip install gevent

celery -A config worker -l info -P gevent
```