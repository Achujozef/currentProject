from django.http import JsonResponse
from django.shortcuts import render
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

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