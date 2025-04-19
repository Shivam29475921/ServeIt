from asgiref.sync import async_to_sync
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from channels.layers import get_channel_layer
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import *
from .forms import *


# Create your views here.

@login_required
def chat_view(request, chatroom_name="public_chat"):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:50]
    form = ChatMessageCreateForm()

    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break

    if chat_group.groupchat_name:
        if request.user not in chat_group.members.all():
            chat_group.members.add(request.user)
    if request.htmx:
        form = ChatMessageCreateForm(request.POST)
        if form.is_valid:
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {
                'message': message,
                'user': request.user,

            }
            return render(request, 'a_rtchat/partials/chat_message_p.html', context)

    context = {
        'chat_messages': chat_messages,
        'form': form,
        'other_user': other_user,
        'chatroom_name': chatroom_name,
        'chat_group': chat_group,

    }
    return render(request, 'a_rtchat/chat.html', context)


@login_required
def get_or_create_chatroom(request, username):
    if request.user.username == username:
        return redirect('home')
    other_user = User.objects.get(username=username)
    my_chatrooms = request.user.chat_groups.filter(is_private=True)

    if my_chatrooms.exists():
        for chatroom in my_chatrooms:
            if other_user in chatroom.members.all():
                chatroom = chatroom
                break
            else:
                chatroom = ChatGroup.objects.create(is_private=True)
                chatroom.members.add(other_user, request.user)
    else:
        chatroom = ChatGroup.objects.create(is_private=True)
        chatroom.members.add(other_user, request.user)

    return redirect('chatroom', chatroom.group_name)


def create_groupchat(request):
    form = NewGroupForm()
    if request.method == "POST":
        form = NewGroupForm(request.POST)
        if form.is_valid():
            new_groupchat = form.save(commit=False)
            new_groupchat.admin = request.user
            new_groupchat.save()
            new_groupchat.members.add(request.user)
            return redirect('chatroom', new_groupchat.group_name)

    context = {
        'form': form,
    }
    return render(request, 'a_rtchat/create_groupchat.html', context)


@login_required
def edit_chatroom(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    if request.user != chat_group.admin:
        raise Http404()
    invite_username = request.POST.get('invite_username')
    if invite_username:
        try:
            user_to_invite = User.objects.get(username=invite_username)
            if user_to_invite not in chat_group.members.all():
                chat_group.members.add(user_to_invite)

                # Send DM with invite link
                dm_group = ChatGroup.objects.filter(is_private=True, members=user_to_invite).filter(members=request.user).first()
                if not dm_group:
                    dm_group = ChatGroup.objects.create(is_private=True)
                    dm_group.members.add(user_to_invite, request.user)

                GroupMessage.objects.create(
                    author=request.user,
                    group=dm_group,
                    body=f"You’ve been invited to join the group chat '{chat_group.groupchat_name or chat_group.group_name}'. Click here to join: /chat/{chat_group.group_name}/"
                )

                messages.success(request, f"{invite_username} has been added.")
            else:
                messages.info(request, f"{invite_username} is already a member.")
        except Exception:
            messages.error(request, f"No user found with username '{invite_username}'.")
    form = ChatRoomEditForm(instance=chat_group)
    if request.method == "POST":
        form = ChatRoomEditForm(request.POST, instance=chat_group)
        if form.is_valid():
            form.save(commit=True)

            remove_members = request.POST.getlist('remove_members')
            for member_id in remove_members:
                member = User.objects.get(id=member_id)
                chat_group.members.remove(member)

            return redirect('chatroom', chatroom_name)
    context = {
        'form': form,
        'chat_group': chat_group,
    }

    return render(request, 'a_rtchat/chatroom_edit.html', context)


def delete_chatroom(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    if request.user != chat_group.admin:
        raise Http404()

    if request.method == "POST":
        chat_group.delete()
        messages.success(request, f"Chatroom has been deleted!")
        return redirect('home')

    context = {
        'chat_group': chat_group,
    }
    return render(request, 'a_rtchat/chatroom_delete.html', context)


@login_required
def leave_chatroom(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    if request.user not in chat_group.members.all():
        raise Http404()

    if request.method == "POST":
        chat_group.members.remove(request.user)
        messages.success(request, f"You have left!")
        return redirect('home')
    context = {}
    return render(request, 'a_rtchat/chatroom_leave.html', context)


def chat_file_upload(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    if request.htmx and request.FILES:
        file = request.FILES['file']
        message = GroupMessage.objects.create(
            file=file,
            author=request.user,
            group=chat_group,
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
