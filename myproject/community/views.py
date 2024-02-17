from django.shortcuts import render
from .models import Post

# Create your views here.
def overseas(request):
    posts = Post.objects.filter(type=0)
    context ={
        'posts': posts
    }
    return render(request, 'community/overseas.html', context=context)

def domestic(request):
    context ={

    }
    return render(request, 'community/domestic.html', context=context)

def write(request):
    return render(request, 'community/writepost.html')\
    
def check(request):
    if request.method == "POST":
        print(request.POST)
        print(request.POST['content'])
    return render(request, 'community/check.html')