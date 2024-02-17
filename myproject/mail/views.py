from django.shortcuts import render, get_object_or_404
from .models import Mail
from home.models import CustomUser
from django.http import JsonResponse

##### 쪽지
# 받은 전체 조회
def mail_receive_list(request):
    user = request.user
    page = int(request.GET.get('page', ''))
    received_mails = Mail.objects.filter(receiver=user).order_by('-timestamp')
    pagination_nums = (len(received_mails)//10)+1
    received_mails = received_mails[(page-1)*10:page*10]
    context = {
        'received_mails':received_mails,
        'pagination_nums':pagination_nums,
        'page':page,
    }
    return render(request, 'mail/mail_receive_list.html', context=context)

# 받은 메일 확인
def mail_receive_detail(request, id):
    received_mail = Mail.objects.filter(id=id).first()
    received_mail.is_read = True
    received_mail.save()
    context = {
        'received_mail':received_mail,
    }
    return render(request, 'mail/mail_receive_detail.html', context=context)

# 보낸 전체 조회
def mail_sent_list(request):
    user = request.user
    sent_mails = Mail.objects.filter(sender=user).order_by('-timestamp')
    pagination_nums = (len(sent_mails)//10)+1
    context = {
        'sent_mails':sent_mails,
        'pagination_nums':pagination_nums,
    }
    return render(request, 'mail/mail_sent_list.html', context=context)

# 보낸 메일 확인
def mail_sent_detail(request, id):
    sent_mail = Mail.objects.filter(id=id).first()
    context = {
        'sent_mail':sent_mail,
    }
    return render(request, 'mail/mail_sent_detail.html', context=context)

# 작성 화면
def mail_write(request): 
    return render(request, 'mail/mail_write.html')

# 작성한 쪽지 전송 가능 체크
def mail_write_check(request): 
    if request.method == 'POST':
        user = request.user
        receiver = request.POST.get('receiver')
        subject = request.POST.get('subject')
        content = request.POST.get('content')
        print(receiver,subject,content)

        receiver_real = CustomUser.objects.filter(username=receiver).first()
        if receiver_real is not None:
            mail = Mail.objects.create(
                sender=user,
                receiver=receiver_real,
                subject = subject,
                content = content,
                )
            mail.save()
            msg = {
                'status': "success",
                'msg' : "쪽지가 성공적으로 전송되었습니다"
                }
            return JsonResponse(msg)
        else:
            print("없는 계정")
            msg = {
                'status': "fail",
                'msg' : "받는 사람에 해당 하는 계정이 존재하지 않습니다"
                }
            return JsonResponse(msg)
    