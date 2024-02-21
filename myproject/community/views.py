from django.shortcuts import render
from .models import Post, Comment
import json
from django.http import JsonResponse

# Create your views here.
def overseas(request):
    posts = Post.objects.filter(type=0).order_by("-timestamp")
    pagination_nums = ((len(posts)-1)//10)+1
    
    if len(posts)==0:
        pagination_nums=1
    page = int(request.GET.get('page', ''))
    print('post개수',len(posts))
    print('pagination_nums',pagination_nums)
    context ={
        'posts': posts,
        'pagination_nums':pagination_nums,
        'page':page,
    }
    return render(request, 'community/overseas.html', context=context)

def domestic(request):
    context ={

    }
    return render(request, 'community/domestic.html', context=context)

def write(request):
    type = int(request.GET.get("type"))
    context ={
        'type':type
    }
    return render(request, 'community/writepost.html',context=context)
    
def check(request):
    if request.method == "POST":
        type = request.POST.get("type")
        if type=="talk":
            type = 2
        elif type=="overseas":
            type=0
        elif type=="domestic":
            type=1
        subject = request.POST.get("subject")
        content = request.POST.get("content")
        writing_post = Post.objects.create(
            type=type,
            author=request.user,
            subject=subject,
            content=content,
        )
        writing_post.save()
        post = writing_post
        comments = Comment.objects.filter(post=post.id, parent_comment=None).order_by("timestamp")
        context ={
            'post': post,
            'comments':comments
        }
    return render(request, 'community/post.html', context=context)

def post(request, id):
    post = Post.objects.filter(id=id).first()
    comments = Comment.objects.filter(post=id, parent_comment=None).order_by("timestamp")
 
    context ={
        'post': post,
        'comments':comments
    }
    return render(request, 'community/post.html', context=context)

def likeit(request):
    post_id = request.GET.get('postid')
    post = Post.objects.filter(id=post_id).first()
    if post.likes.filter(pk=request.user.id).exists():
        post.likes.remove(request.user)
        post.save()   
    else:
        post.likes.add(request.user)
        post.save()
    like_num = len(post.likes.all())
    response_data = {
        'post_id': post_id,
        'like_num':like_num
    }
    return JsonResponse(response_data)

def commenting(request):
    post_id = request.POST.get('postid')
    post = Post.objects.filter(id=post_id).first()
    my_comment = request.POST.get('my_comment')
    comment = Comment.objects.create(
        post=post,
        author=request.user,
        content=my_comment
    )
    comment.save()
    
    response_data = {
        'success':"success"  
    }
    return JsonResponse(response_data)

def recommenting(request, id):
    recomment = request.POST.get("my_recomment")
    recomment_id = int(request.POST.get("recomment_id"))
    post_id = id
    parent_comment = Comment.objects.filter(id=recomment_id).first()
    post = Post.objects.filter(id=post_id).first()

    comment = Comment.objects.create(
        post=post,
        author=request.user,
        parent_comment=parent_comment,
        content=recomment
    )
    comment.save()

    comments = Comment.objects.filter(post=post_id, parent_comment=None).order_by("timestamp")
 
    context ={
        'post': post,
        'comments':comments
    }
    return render(request, 'community/post.html', context=context)