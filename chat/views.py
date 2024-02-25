from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Room, Message, Friends, Friend_Requests
from django.db.models import Q
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from services.addFriend import AddFriend
from services.check_model import get_or_none
from complaint.models import Complaint
from complaint.forms import ComplaintForm


Users = get_user_model()


@login_required
def index(request):
    return render(request, 'chat/index.html', {})


@login_required(login_url='/account/login/')
def start_chat(request, user):
    get_user = Users.objects.get(username=request.user)
    second_user = Users.objects.get(username=user)

    if Friends.objects.filter(user=get_user, friend_user=second_user).exists():
        try:
            room = Room.objects.get(first_user=request.user, second_user=second_user)
        except Room.DoesNotExist:
            try:
                room = Room.objects.get(first_user=second_user, second_user=request.user)
            except Room.DoesNotExist:
                room = Room.objects.create(first_user=request.user, second_user=second_user)

        return redirect(f'/room/{str(room.room_code)}/')
    else:
        return redirect('/')


@login_required(login_url='/account/login/')
def room(request, room_code):
    users = Users.objects.all().exclude(username=request.user)

    try:
        room = get_object_or_404(Room, room_code=room_code)
    except Http404:
        return redirect('/')

    if room.first_user == request.user or room.second_user == request.user:
        complaint_form = ComplaintForm()

        if request.POST and 'room_user_id' in request.POST:
            complaint_form = ComplaintForm(data=request.POST, request=request)


            if complaint_form.is_valid():
                room_user = Users.objects.get(id=request.POST.get('room_user_id'))
                get_user = Users.objects.get(username=request.user.username)

                Complaint.objects.create(from_user=get_user,
                                         to_user=room_user,
                                         compliant_reason=request.POST.get('compliant_reason'),
                                         content=request.POST.get('content'))

                if Complaint.objects.filter(to_user=room_user).count() >= 5:
                    get_user = Users.objects.get(username=room_user)
                    get_user.status = 'Unavailable'
                    get_user.is_active = False
                    get_user.save()

                return redirect('/')


        messages = Message.objects.filter(Q(room=room_code)&Q(visibility='visible'))

        player_types = ['mp4', 'mkv', 'mov', 'avi', 'mp3', 'mpeg', 'oog']
        file_types = ['pdf', 'zip', 'rar', 'txt', 'doc', 'docx', 'rtf', 'xls', 'xlsx', 'ppt', 'pptx'];

        context = {
            'users': users,
            'room': room,
            'room_user': room.second_user if room.first_user == request.user else room.first_user,
            'room_code': room_code,
            'messages_m': messages,
            'player_types': player_types,
            'file_types': file_types,
            'complaint_form': complaint_form,
        }

        return render(request, 'chat/room.html', context)

    else:
        return redirect('/')

@login_required(login_url='/account/login/')
def delete_message(request):
    data = {}

    user = get_object_or_404(Users, username=request.user)
    message = get_object_or_404(Message, id=int(request.POST.get('messageID')))

    if user == message.user:
        message.visibility = 'invisible'
        message.save()
        data['success'] = 'Message deleted successfully'
    else:
        data['error'] = 'Message could not be deleted.'

    return JsonResponse(data)


@login_required(login_url='/account/login')
def remove_friend(request):
    data = {}

    get_user = Users.objects.get(username=request.user)
    get_id = int(request.POST.get('friendID'))

    get_friend_user = get_or_none(Users, id=get_id)

    if get_friend_user:
        if get_or_none(Friends, user=get_user, friend_user=get_friend_user):
            get_friend = Friends.objects.get(user=get_user, friend_user=get_friend_user)
            get_friend.friend_user.remove(get_friend_user)

            get_request_user_friend = Friends.objects.get(user=get_friend_user, friend_user=get_user)
            get_request_user_friend.friend_user.remove(get_user)

            data['success'] = get_friend_user.id

            room_query_1 = get_or_none(Room, first_user=get_user, second_user=get_friend_user)
            room_query_2 = get_or_none(Room, first_user=get_friend_user, second_user=get_user)

            if room_query_1:
                room_query_1.delete()
            elif room_query_2:
                room_query_2.delete()

    return JsonResponse(data)


def accept_invite(request):
    data = {}

    get_id = request.POST.get('id')

    getUser = Users.objects.get(username=request.user)
    get_friend_request_obj = get_or_none(Friend_Requests, id=get_id, to_user=getUser)

    if get_friend_request_obj:
        get_request_user = get_friend_request_obj.from_user
        AddFriend.add_friend(getUser, get_request_user)

        data['success'] = get_friend_request_obj.id
        get_friend_request_obj.delete()
        # delete friend request object because user added to friend list

    return JsonResponse(data)


def deny_invite(request):
    data = {}

    get_id = int(request.POST.get('id'))
    getUser = Users.objects.get(username=request.user)

    get_friend_request_obj = get_or_none(Friend_Requests, id=get_id, to_user=getUser)

    if get_friend_request_obj:
        data['success'] = get_friend_request_obj.id
        get_friend_request_obj.delete()

    return JsonResponse(data)


def cancel_invite(request):
    data = {}
    get_id = int(request.POST.get('id'))

    getUser = Users.objects.get(username=request.user)
    get_friend_request_obj = get_or_none(Friend_Requests, id=get_id, from_user=getUser)

    if get_friend_request_obj:
        data['success'] = get_friend_request_obj.id
        get_friend_request_obj.delete()

    return JsonResponse(data)
