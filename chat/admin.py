from django.contrib import admin
from .models import Room, Message, Friends, Friend_Requests

class RoomAdmin(admin.ModelAdmin):
    list_display = ['first_user', 'second_user']

admin.site.register(Room, RoomAdmin)

class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'room']

admin.site.register(Message, MessageAdmin)

admin.site.register(Friends)

admin.site.register(Friend_Requests)