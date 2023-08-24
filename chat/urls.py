from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='user'),
    path('start_chat/<str:user>/', views.start_chat, name='start_chat'),
    path('room/<str:room_code>/', views.room, name='room'),
    path('delete-message/', views.delete_message, name='delete-message'),
    path('remove-friend/', views.remove_friend, name='remove-friend'),
    path('accept-invite/', views.accept_invite, name='accept-invite'),
    path('deny-invite/', views.deny_invite, name='deny-invite'),
    path('cancel-invite/', views.cancel_invite, name='cancel-invite'),
]
