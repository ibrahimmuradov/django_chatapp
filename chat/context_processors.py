from django.contrib.auth import get_user_model
from .forms import UserEditForm
from .models import Room, Friends, Friend_Requests
from django.contrib import messages
from django.db.models import Q
from services.addFriend import AddFriend
from .get_message_type import message_type


Users = get_user_model()

def user_context_processor(request):
    context = {}

    if request.user.is_authenticated:
        get_full_url = request.build_absolute_uri() # get full url
        getUser = Users.objects.get(username=request.user)

        incoming_invitation = Friend_Requests.objects.filter(to_user=getUser)
        context['incoming_invitations'] = incoming_invitation


        outgoing_invitation = Friend_Requests.objects.filter(from_user=getUser)
        context['outgoing_invitations'] = outgoing_invitation

        get_friend_objs = Friends.objects.get(user=getUser) if Friends.objects.filter(user=getUser).exists() else False

        if get_friend_objs:
            friends_and_rooms_message = {}

            for friend in get_friend_objs.friend_user.all():
                if Room.objects.filter(first_user=friend, second_user=getUser):
                    getRoom = Room.objects.get(first_user=friend, second_user=getUser)
                    getLastObj = getRoom.message_set.last()

                    getLastMessage = message_type(message_obj=getLastObj)

                elif Room.objects.filter(first_user=getUser, second_user=friend):
                    getRoom = Room.objects.get(first_user=getUser, second_user=friend)
                    getLastObj = getRoom.message_set.last()

                    getLastMessage = message_type(message_obj=getLastObj)

                else:
                    getLastMessage = None

                friends_and_rooms_message[friend] = getLastMessage

            context['friends_and_rooms_message'] = friends_and_rooms_message

        if request.method == "POST" and 'username' in request.POST:
            user_edit_form = UserEditForm(instance=request.user, data=request.POST, files=request.FILES, request=request)
            if user_edit_form.is_valid():
                user_edit_form.save()
        else:
            user_edit_form = UserEditForm(instance=request.user)

        context['user_form'] = user_edit_form

        if request.method == "POST" and 'friend_user' in request.POST:
            friend_user = request.POST.get('friend_user')

            if Users.objects.filter(username=friend_user).exists():
                get_request_user = Users.objects.get(username=friend_user)
                if get_request_user == getUser: # check user send invite to himself
                    messages.error(request, 'You cannot send yourself a friend invite')
                else:
                    if Friends.objects.filter(Q(user=getUser)&Q(friend_user=get_request_user)).exists():
                        # check already added user friend
                        messages.error(request, 'This user has already been added as your friend')
                    else:
                        if Friend_Requests.objects.filter(Q(from_user=getUser)&Q(to_user=get_request_user)).exists():
                            # check already invited user
                            messages.error(request, 'You have already invited this user')
                        elif Friend_Requests.objects.filter(Q(from_user=get_request_user)&Q(to_user=getUser)).exists():
                            AddFriend.add_friend(getUser, get_request_user)

                            get_friend_obj = Friend_Requests.objects.get(Q(from_user=get_request_user)&Q(to_user=getUser))
                            get_friend_obj.delete()
                            # delete friend request object because user added to friend list
                            context['refresh'] = get_full_url

                        else:
                            Friend_Requests.objects.create(from_user=getUser, to_user=get_request_user)
                            # create a new invitation if the user has not sent an invitation
                            context['refresh'] = get_full_url

            else:
                messages.error(request, 'Username does not exist')

    return context
