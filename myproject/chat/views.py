from django.shortcuts import render, HttpResponseRedirect
from .models import ChatRoom

# Create your views here.
def chat(request):
    chatrooms = ChatRoom.objects.all()
    context = {
        'chatrooms':chatrooms
    }
    return render(request, 'chat/chat.html',context=context)

def chat_start(request):
    return render(request, 'chat/chat_start.html')

def chat_check(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        limit = request.POST.get("limit")
        owner = request.user

        #방만들기
        chatroom = ChatRoom.objects.create(
            title = title,
            limit = limit,
            owner = owner,
        )
        chatroom.save()
        room_id = chatroom.id
        return HttpResponseRedirect(f'/chat/{room_id}')
    else:
        return "error"

def chat_room(request, room_id):
    chatroom = ChatRoom.objects.filter(id=room_id).first()

    context = {
        'chatroom':chatroom,
    }
    return render(request, 'chat/chat_room.html', context)