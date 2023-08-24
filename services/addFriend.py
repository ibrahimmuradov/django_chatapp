from chat.models import Friends

class AddFriend:
    @staticmethod
    def add_friend(user, friendUser):
        from_user_friend_obj = Friends.objects.get(user=user) if Friends.objects.filter(
            user=user).exists() else False
        to_user_friend_obj = Friends.objects.get(user=friendUser) if Friends.objects.filter(
            user=friendUser).exists() else False

        if from_user_friend_obj:
            from_user_friend_obj.friend_user.add(friendUser)
            # If the user has friends, add them
        else:
            from_friend_obj = Friends.objects.create(user=user)
            from_friend_obj.friend_user.add(friendUser)
            # If the user has no friends, create model

        if to_user_friend_obj:
            to_user_friend_obj.friend_user.add(user)
            # also add the inviting user to the other user's friend list
        else:
            to_friend_obj = Friends.objects.create(user=friendUser)
            to_friend_obj.friend_user.add(user)

        pass