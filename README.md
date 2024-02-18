# <img src="https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white"/> Django-project
## 🔎개요
장고를 활용한 웹 사이트를 제작 연습입니다.

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
- 게시물 기능
- API 활용 기능
- 쪽지 기능
- 실시간 채팅 기능

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



## 3. 게시물 기능

<img width="591" alt="image" src="https://github.com/SHINDongHyeo/Django-project/assets/96512568/90de5245-2740-49eb-8318-286fe58eb4e2">

- 설명

일반적인 커뮤니티에 존재하는 게시물과 같이 유저가 게시물을 작성할 수 있고, 해당 게시물을 여러 유저가 '좋아요'를 눌러 추천할 수 있는 기능을 구현

- ERD




## 4. API 활용 기능

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





## 5. 쪽지 기능

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

## 6. 실시간 채팅 기능

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



