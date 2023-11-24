# chat_service/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('chat-partners/<int:user_id>/', ChatPartnersView.as_view(), name='chat-partners'),
    path('save-message/<int:user_id>/<int:doctor_id>/', SaveMessageView.as_view(), name='save-message'),
    path('user_chats/<int:user_id>/', UserChatsView.as_view(), name='user_chats'),
    path('chat_messages/<int:chat_id>/', ChatMessagesView.as_view(), name='chat_messages'),
]

