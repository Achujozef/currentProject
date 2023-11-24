from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .pusher import pusher_client

class ChatPartnersView(APIView):
    def get(self, request,user_id):
        chat_partners = set(
            Message.objects.filter(sender_id=user_id).values_list('receiver_id', flat=True) |
            Message.objects.filter(receiver_id=user_id).values_list('sender_id', flat=True)
        )
        return Response({'chat_partners': list(chat_partners)}, status=status.HTTP_200_OK)
    

class SaveMessageView(APIView):
    def post(self, request, user_id, doctor_id):
        data = request.data
        message = request.data['content']
        serializer = MessageSerializer(data=data)
        user_type = request.data['user_type']
        if serializer.is_valid():
            existing_chat = Chat.objects.filter(user_id=user_id, doctor_id=doctor_id).first()

            if existing_chat:
                chat_id = existing_chat.id
            else:
                new_chat = Chat.objects.create(user_id=user_id, doctor_id=request.data['doctor_id'])
                chat_id = new_chat.id
            serializer.validated_data['chat_id'] = chat_id
            serializer.validated_data['user_type'] = user_type 
            serializer.save()
            print('chat_id',chat_id)
            pusher_client.trigger(f'chat_{chat_id}', 'message', {
                'message': message,
            })
            return Response({'chat_id': chat_id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserChatsView(APIView):
    def get(self, request, user_id):
        user_chats = Chat.objects.filter(models.Q(user_id=user_id) | models.Q(doctor_id=user_id))
        serializer = ChatSerializer(user_chats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ChatMessagesView(APIView):
    def get(self, request, chat_id):
        chat_messages = Message.objects.filter(chat_id=chat_id)
        serializer = MessageSerializer(chat_messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
