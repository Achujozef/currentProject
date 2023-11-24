from django.shortcuts import get_object_or_404, render
from twilio.rest import Client
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from twilio.rest import Client
from rest_framework import status
from .serializers import NotificationSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import random
import requests
from .models import *

class SendOtpTwlioMessages(APIView):
    def post(self, request, *args, **kwargs):
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        recipient_phone_numbers = request.data.get('recipient_phone_numbers', [])
        message_content = request.data.get('message_content', '')

        responses = []

        for recipient_phone_number in recipient_phone_numbers:
            message = client.messages.create(
                to=recipient_phone_number,
                from_=settings.TWILIO_PHONE_NUMBER,
                body=message_content
            )

            if message.sid:
                responses.append({"recipient": recipient_phone_number, "status": "Message sent successfully"})
            else:
                responses.append({"recipient": recipient_phone_number, "status": "Error sending message"})

        return Response(responses)


class SendWhatsAppMessageTwilio(APIView):
    def post(self, request, *args, **kwargs):
        try:
            account_sid = 'AC973ffa35c71fb96c3b0c2bb397d11dd0'
            auth_token = '038dd559482b771993eddcfa2bf5876e'
            client = Client(account_sid, auth_token)
            link = request.data.get('link', '')  
            body = f'Your consulting has started. Click the link below to join: {link}'
            to_number = 'whatsapp:+917736448062'
            message = client.messages.create(
                from_='whatsapp:+14155238886',
                body=body,
                to=to_number,
                status_callback='http://localhost:8009/api/send-whatsapp-message/'
                # status_callback='https://2d50-116-68-72-251.ngrok.io/api/send-whatsapp-message/'

            )
            return Response({'message_sid': message.sid}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class SendOTPView(viewsets.GenericViewSet):
    def send_otp(self, phone_num, otp):
        url = 'https://www.fast2sms.com/dev/bulkV2'
        payload = f'sender_id=TXTIND&message={otp}&route=v3&language=english&numbers={phone_num}'
        headers = {
            'authorization': "mEgP0Z5wnldKSerOu1GW8qUbVctH3jkYaM7QCI4Jzp69XNT2ALFmiofRb467D0rSOWVB3qp8J5HYeIvt",
            'Content-Type': "application/x-www-form-urlencoded"
        }
        response = requests.request("POST", url, data=payload, headers=headers)

    def generate_otp(self):
        return str(random.randint(1000, 9999))

    def create(self, request):
        phone_num = request.data.get('phone_num')
        otp = self.generate_otp()
        self.send_otp(phone_num, otp)

        return Response({'otp': otp}, status=status.HTTP_201_CREATED)
    

class NotificationListCreateView(APIView):
    def get(self, request, user_id):
        notifications = Notification.objects.filter(user_id=user_id).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

class NotificationDetailView(APIView):
    def delete(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Notification.DoesNotExist:
            return Response({"detail": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)
        

class NotificationClearView(APIView):
    def delete(self, request, user_id):
        notifications = Notification.objects.filter(user_id=user_id)
        notifications.delete()
        return Response({"message": "Notifications deleted successfully"}, status=status.HTTP_200_OK)
    

class NotificationDeleteView(APIView):
    def delete(self, request, notification_id):
        notification = get_object_or_404(Notification, id=notification_id)
        notification.delete()
        return Response({"message": "Notification deleted successfully"}, status=status.HTTP_200_OK)