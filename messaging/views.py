from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .forms import UserSearchForm


@login_required
def inbox(request):
    form = UserSearchForm(request.GET or None)
    requested_users = None
    users_searched = False
    if form.is_valid():
        query = form.cleaned_data.get("query")
        if query:
            requested_users = User.objects.filter(
                username__icontains=query
            ).values_list("username", flat=True)
            users_searched = True

    conversation_history = {}
    messages_history = Message.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)
    ).order_by("timestamp")

    for message in messages_history:
        messaging_partner = (
            message.sender.username + message.recipient.username
        ).replace(request.user.username, "")
        if users_searched and messaging_partner not in requested_users:
            continue
        conversation_history[messaging_partner] = {
            "sender": message.sender.username,
            "recipient": message.recipient.username,
            "content": message.content,
            "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }

    start_conversations = []
    if users_searched:
        for username in requested_users:
            if (
                username != request.user.username
                and username not in conversation_history
            ):
                start_conversations.append(username)
    return render(
        request,
        "messaging/inbox.html",
        {
            "form": form,
            "conversation_history": conversation_history,
            "start_conversations": start_conversations,
        },
    )


@login_required
def direct_messaging(request, messaging_partner_name):
    messaging_partner = get_object_or_404(User, username=messaging_partner_name)
    messages_history = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=messaging_partner))
        | Q(sender=messaging_partner) & Q(recipient=request.user)
    ).order_by("timestamp")
    messages_data = [
        {
            "sender": message.sender.username,
            "recipient": message.recipient.username,
            "content": message.content,
            "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for message in messages_history
    ]
    return render(
        request,
        "messaging/direct_messaging.html",
        {"messages": messages_data, "messaging_partner": messaging_partner.username},
    )


@login_required
@csrf_exempt
def send_message(request, recipient_username):
    recipient = get_object_or_404(User, username=recipient_username)
    if request.method == "POST":
        content = request.POST["content"]
        if content:
            Message.objects.create(
                sender=request.user, recipient=recipient, content=content
            )
            return JsonResponse({"status": "Message sent"})
    return render(request, "messaging/send_message.html", {"recipient": recipient})


@login_required
def get_new_messages(request, messaging_partner_name):
    messaging_partner = get_object_or_404(User, username=messaging_partner_name)
    messages_history = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=messaging_partner))
        | Q(sender=messaging_partner) & Q(recipient=request.user)
    ).order_by("timestamp")
    messages_data = [
        {
            "sender": message.sender.username,
            "recipient": message.recipient.username,
            "content": message.content,
            "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for message in messages_history
    ]
    return JsonResponse({"messages": messages_data})
