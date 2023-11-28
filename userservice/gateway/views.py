from django.http import JsonResponse
from django.shortcuts import render
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from api.models import *
@permission_classes([IsAuthenticated])
class FeedsView(APIView):
    def get(self, request):
        try:
            user_id = request.GET.get('user_id')
            response = requests.get(f'http://postservice:8002/api/packeposts/?user_id={user_id}')
            return Response(response.json())
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes([IsAuthenticated])
class LikeDislikePostView(APIView):
    def post(self, request, post_id):
        user_id = request.GET.get('user_id', None)
        try:
            response = requests.post(
                f'http://postservice:8002/api/posts/{post_id}/like-dislike/?user_id={user_id}')
            response.raise_for_status()  # Raise an exception for HTTP errors
            return Response(response.json(), status=response.status_code)
        except requests.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes([IsAuthenticated])
class ApiGatewayView(APIView):
    def list_all_posts(self, request):
        try:
            response = requests.get('http://postservice:8002/api/posts/')
            return Response(response.json(), status=response.status_code)
        except requests.RequestException as e:
            return Response({'error': str(e)}, status=500)

    def create_post(self, request):
        try:
            response = requests.post('http://postservice:8002/api/posts/', json=request.data)
            return Response(response.json(), status=response.status_code)
        except requests.RequestException as e:
            return Response({'error': str(e)}, status=500)

    def list_posts_by_doctor(self, request, doctor_id):
        try:
            response = requests.get(f'http://postservice:8002/api/posts/by-doctor/{doctor_id}/')
            return Response(response.json())
        except requests.RequestException as e:
            return Response({'error': str(e)}, status=500)

    def delete_post(self, request, post_id):
        try:
            response = requests.delete(f'http://postservice:8002/api/posts/{post_id}/')
            return Response({}, status=response.status_code)
        except requests.RequestException as e:
            return Response({'error': str(e)}, status=500)

    def get(self, request,doctor_id):
        return self.list_posts_by_doctor(request, doctor_id)

    def post(self, request):
        return self.create_post(request)

    def delete(self, request, post_id):
        return self.delete_post(request, post_id)


@permission_classes([IsAuthenticated])
class GetMessageView(APIView):
    def get(self, request,chat_id):
        try:
            response = requests.get(f'http://chatservice:8004/api/chat_messages/{chat_id}')
            return Response(response.json())
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes([IsAuthenticated])
class GetNotificationView(APIView):
    def get(self, request):
        user_id = request.user.id
        try:
            response = requests.get(f'http://notificationservice:8005/api/notifications/{user_id}')
            return Response(response.json())
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes([IsAuthenticated])
class ClearNotificationView(APIView):
    def delete(self, request):
        user_id = request.user.id
        try:
            response = requests.delete(f'http://notificationservice:8005/api/clear-notifications/{user_id}')
            return Response(response.json())
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes([IsAuthenticated])
class DeleteNotificationView(APIView):
    def delete(self, request,notification_id):
        try:
            response = requests.delete(f'http://notificationservice:8005/api/delete-notification/{notification_id}')
            return Response(response.json())
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes([IsAuthenticated])
class FollowerPostApiView(APIView):
    def get(self, request, *args, **kwargs):
        follower_ids = Follower.objects.filter(user=request.user).values_list('doctor_id', flat=True)
        user_id = request.user.id
        postservice_url = 'http://postservice:8002/api/follower-post'  
        payload = {'doctor_ids': follower_ids, 'user_id': user_id}
        try:
            response = requests.get(postservice_url, params=payload)
            if response.status_code == status.HTTP_200_OK:
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Failed to fetch posts from postservice'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.RequestException as e:
            return Response({'error': f'Error making request to postservice: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes([IsAuthenticated])
class GetSlotByDoctorView(APIView):
    def get(self, request,doctor_id):
        print("reached the View")
        try:
            print("reached the try")
            response = requests.get(f'http://appointmentservice:8003/api/list-slots/{doctor_id}')
            print("The Response is ",response.json())
            return Response(response.json())
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes([IsAuthenticated])
class SlotBookingView(APIView):
    def post(self, request, slot_id):
        user_id = request.user.id
        try:
            response = requests.post(
                f'http://appointmentservice:8003/api/book-appointment/{slot_id}/{user_id}/')
            response.raise_for_status()  # Raise an exception for HTTP errors
            return Response(response.json(), status=response.status_code)
        except requests.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyPaymentView(APIView):
    def post(self, request, *args, **kwargs):
        print("Reached The VerifyPaymentView")
        try:
            razorpay_payment_id = request.data.get('razorpay_paymentId')
            razorpay_order_id = request.data.get('razorpay_orderId')
            razorpay_signature = request.data.get('razorpay_signature')
            print(razorpay_order_id,razorpay_payment_id,razorpay_signature)


            response = requests.post(
                'http://appointmentservice:8003/api/verifySignature/',
                data={
                    'razorpay_paymentId': razorpay_payment_id,
                    'razorpay_orderId': razorpay_order_id,
                    'razorpay_signature': razorpay_signature,
                }
            )


            if response.status_code == 200:
                return Response({'status': 'success'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'failure'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@permission_classes([IsAuthenticated])
class PostCommentView(APIView):
    def post(self, request, post_id):
        user_id = request.user.id
        comment = request.data.get('comment')
        try:
            response = requests.post(
                f'http://postservice:8002/api/create-comment/{post_id}/{user_id}/',
                data={
                    "comment":comment
                })
            response.raise_for_status()  # Raise an exception for HTTP errors
            return Response(response.json(), status=response.status_code)
        except requests.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes([IsAuthenticated])
class GetCommentsView(APIView):
    def get(self, request,post_id):
        try:
            print("reached the try")
            response = requests.get(f'http://postservice:8002/api/get-comments/{post_id}/')
            print("The Response is ",response.json())
            return Response(response.json())
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
