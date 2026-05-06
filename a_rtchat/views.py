from django.shortcuts import render , get_object_or_404 , redirect
from .models import ChatGroup , GroupMessage
from django.contrib.auth.decorators import login_required
from .forms import ChatMessageCreateForm , NewGroupForm
from django.contrib.auth import get_user_model
from django.http import Http404
from django.contrib import messages
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import HttpResponse

# Create your views here.


User = get_user_model()


@login_required
def chat_view(request , chatroom_name='public-chat'):
    
    chat_group = get_object_or_404(ChatGroup , group_name=chatroom_name)
    
    chat_messages = chat_group.chat_messages.all()[:30]
    
    form = ChatMessageCreateForm()
    
    other_user = None
    
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()
        
        for member in chat_group.members.all():
            
            if member != request.user:
                other_user = member
                break
            
    if chat_group.group_name:
        if request.user not in chat_group.members.all():
            if request.user.emailaddress_set.filter(verified=True).exists():
                chat_group.members.add(request.user)
            else:
                messages.warning(request , 'you need to verify email to join chat')
                return redirect('profile-settings')
            
    
    if request.htmx:
        form = ChatMessageCreateForm(request.POST)
        
        if form.is_valid():
            
            message = form.save(commit=False)
            
            message.author = request.user
            
            message.group = chat_group
            
            message.save()
            context = {
                'message':message,
                'user':request.user,
            }
            return render(request , 'a_rtchat/partials/chat_message_p.html' , context)
        
    context = {
        'chat_messages':chat_messages ,
        'form':form,
        'other_user':other_user,
        'chatroom_name':chatroom_name,
        'chat_group':chat_group,
    }
    
    
    return render(request , 'a_rtchat/chat.html' , context)


@login_required
def get_or_create_chatroom(request, username):

    User = get_user_model()

    if request.user.username == username:
        return redirect('home')

    other_user = get_object_or_404(User, username=username)

    my_chatrooms = request.user.chat_groups.filter(is_private=True)

    chatroom = None

    for room in my_chatrooms:
        if other_user in room.members.all():
            chatroom = room
            break

    if not chatroom:
        chatroom = ChatGroup.objects.create(is_private=True)
        chatroom.members.add(other_user, request.user)

    return redirect('chatroom', chatroom.group_name)

@login_required
def create_groupchat(request):
    form = NewGroupForm()
    
    if request.method == 'POST':
        form = NewGroupForm(request.POST)
        if form.is_valid():
            new_groupchat = form.save(commit=False)
            new_groupchat.admin = request.user
            new_groupchat.save()
            new_groupchat.members.add(request.user)
            return redirect('chatroom', new_groupchat.group_name)
    
    context = {
        'form': form
    }
    return render(request , 'a_rtchat/create_groupchat.html' , context)


def chat_file_upload(request , chatroom_name):
    
    chat_group = get_object_or_404(ChatGroup , group_name=chatroom_name)
    
    if request.htmx and request.FILES:
        file = request.FILES['file']
        message = GroupMessage.objects.create(
            file = file,
            author = request.user, 
            group = chat_group,
        )
        channel_layer = get_channel_layer()
        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }
        async_to_sync(channel_layer.group_send)(
            chatroom_name, event
        )
    return HttpResponse()





