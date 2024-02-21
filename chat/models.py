from django.db import models
from services.Date import Date
from services.Uploader import Upload_to
import uuid
from django.contrib.auth import get_user_model

Users = get_user_model()

VISIBILITY = (
    ('visible', 'visible'),
    ('invisible', 'invisible')
)

class Room(Date):
    room_code = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='first_user')
    second_user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='second_user')

    def __str__(self):
        return f'Room: {self.first_user} -- {self.second_user}'

class Message(Date):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to=Upload_to.user_file, null=True, blank=True)
    file_type = models.CharField(max_length=10, null=True, blank=True)
    file_name = models.CharField(max_length=500, null=True, blank=True)
    file_size = models.FloatField(null=True, blank=True)
    visibility = models.CharField(max_length=100, choices=VISIBILITY, default='visible')

    def __str__(self):
        return f'Message: {self.user} -- {self.room}'


class Friend_Requests(Date):
    from_user = models.ForeignKey(Users, related_name='friendships_sent', on_delete=models.CASCADE, null=True, blank=True)
    to_user = models.ForeignKey(Users, related_name='friendships_received', on_delete=models.CASCADE, null=True, blank=True,)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.from_user.username} --> {self.to_user.username}'

    class Meta:
        ordering = ('-created_date', )
        verbose_name = 'Friend Request'
        verbose_name_plural = 'Friend Requests'


class Friends(Date):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True, related_name='User')
    friend_user = models.ManyToManyField(Users, blank=True, related_name='friend_user')

    def __str__(self):
        return f'{self.id} -- {self.user.username}'

    class Meta:
        ordering = ('-created_date', )
        verbose_name = 'Friend'
        verbose_name_plural = 'Friends'
