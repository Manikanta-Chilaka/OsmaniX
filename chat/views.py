from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Conversation, Message
from django.http import JsonResponse
from django.db.models import Max
@login_required
def start_chat(request, username):
    other_user = get_object_or_404(User, username=username)

    if other_user == request.user:
        return redirect('profile_detail', username=username)

    # Check if conversation already exists
    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).first()

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)

    return redirect('chat_detail', conversation_id=conversation.id)

@login_required
def inbox(request):
    conversations = request.user.conversations.all().order_by('-created_at')
    return render(request, 'chat.html', {
        'conversations': conversations
    })


@login_required
def chat_detail(request, conversation_id):
    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        participants=request.user
    )

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                text=text
            )
        return redirect('chat_detail', conversation_id=conversation.id)

    messages = conversation.messages.order_by('created_at')

    return render(request, 'chat_detail.html', {
        'conversation': conversation,
        'messages': messages
    })


@login_required
def fetch_messages(request, conversation_id):
    conversation = get_object_or_404(
        Conversation,
        id=conversation_id,
        participants=request.user
    )

    messages = conversation.messages.order_by('created_at')

    data = []
    for msg in messages:
        data.append({
            'sender': msg.sender.username,
            'text': msg.text,
            'time': msg.created_at.strftime('%H:%M')
        })

    return JsonResponse(data, safe=False)


@login_required
def inbox_data(request):
    conversations = (
        request.user.conversations
        .annotate(last_time=Max('messages__created_at'))
        .order_by('-last_time')
    )

    data = []

    for convo in conversations:
        last_msg = convo.messages.last()
        other_user = convo.participants.exclude(id=request.user.id).first()

        data.append({
            'conversation_id': convo.id,
            'username': other_user.username if other_user else '',
            'initial': other_user.username[0].upper() if other_user else '',
            'last_message': last_msg.text if last_msg else 'No messages yet',
            'is_me': last_msg.sender_id == request.user.id if last_msg else False,
            'time': last_msg.created_at.strftime('%H:%M') if last_msg else '',
        })

    return JsonResponse(data, safe=False)

