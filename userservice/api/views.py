from django.http import Http404

from django.contrib.auth import authenticate
import requests
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .services import *
from .models import * 
from .serializer import *

class UserAccountCreateView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserCreateSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.create(serializer.validated_data)

        user = UserAccountSerializer(user)

        return Response(user.data, status=status.HTTP_201_CREATED)



@permission_classes([IsAuthenticated])
class UserDocumentListView(APIView):
    def list(self, request):
        list_service = UserDocumentListService()
        user_documents = list_service.list_user_documents()
        serialized_data = UserDocumentSerializer(user_documents, many=True)
        return Response(serialized_data.data)
    

@permission_classes([IsAuthenticated])
class UserDocumentCreateView(APIView):
    def create(self, request):
        create_service = UserDocumentCreateService()
        serialized_data = UserDocumentSerializer(data=request.data)
        if serialized_data.is_valid():
            user_document = create_service.create_user_document(request.data)
            return Response(UserDocumentSerializer(user_document).data, status=status.HTTP_201_CREATED)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class UserDocumentRetrieveView(APIView):
    def retrieve(self, request, pk=None):
        retrieve_service = UserDocumentRetrieveService()
        user_document = retrieve_service.get_user_document(pk)
        if not user_document:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(UserDocumentSerializer(user_document).data)


@permission_classes([IsAuthenticated])
class UserDocumentUpdateView(APIView):
    def update(self, request, pk=None):
        update_service = UserDocumentUpdateService()
        user_document = update_service.get_user_document(pk)
        if not user_document:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serialized_data = UserDocumentSerializer(user_document, data=request.data)
        if serialized_data.is_valid():
            user_document = update_service.update_user_document(user_document, request.data)
            return Response(UserDocumentSerializer(user_document).data, status=status.HTTP_202_ACCEPTED)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class UserDocumentDestroyView(APIView):
    def destroy(self, request, pk=None):
        delete_service = UserDocumentDeleteService()
        user_document = delete_service.get_user_document(pk)
        if not user_document:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        delete_service.delete_user_document(user_document)
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes([IsAuthenticated])
class ChangePasswordView(APIView):
    def post(self, request):
        new_password = request.data.get('new_password')
        change_password_service = ChangePasswordService()
        change_password_service.change_password(request.user, new_password)
        return Response({'message': 'Password changed successfully'})


@permission_classes([IsAuthenticated])
class ChangePhoneNumberView(APIView):
    def post(self, request):
        new_phone_number = request.data.get('new_phone_number')
        change_phone_number_service = ChangePhoneNumberService()
        change_phone_number_service.change_phone_number(request.user, new_phone_number)
        return Response({'message': 'Phone number changed successfully'})


@permission_classes([IsAuthenticated])
class ChangePhotoView(APIView):
    def post(self, request):
        new_photo = request.data.get('new_photo')
        change_photo_service = ChangePhotoService()
        change_photo_service.change_photo(request.user, new_photo)
        return Response({'message': 'Photo changed successfully'})


class EditUserProfileView(APIView):

    def patch(self, request, *args, **kwargs):
        user = request.user

        # Get data from request
        name = request.data.get('name')
        email = request.data.get('email')
        phonenumber = request.data.get('phonenumber')
        image = request.data.get('image')

        # Validate data if needed

        # Update user details
        user.name = name if name is not None else user.name
        user.email = email if email is not None else user.email
        user.phonenumber = phonenumber if phonenumber is not None else user.phonenumber

        if image:
            user.image = image

        user.save()

        serializer = UserAccountSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

@permission_classes([IsAuthenticated])
class GetUser(APIView):
    def get(self,request):
        try:
            user = request.user
            serializer = UserAccountSerializer(user)
            return Response(serializer.data)        
        except UserAccount.DoesNotExist:
            raise Http404
            

@permission_classes([IsAuthenticated])
class UserSearchView(APIView):
    def get(self, request):
        keyword = request.GET.get('query')
        users = UserAccount.objects.filter(Q(name__icontains = keyword) | Q(phonenumber__icontains = keyword) , is_staff = False)
        serialized = UserAccountSerializer(users, many=True)
        return Response(serialized.data)



@permission_classes([IsAuthenticated])
class FollowDoctorView(APIView):
    def post(self, request, doctor_id):
        doctor_service = DoctorService()
        doctor = doctor_service.get_doctor_by_id(doctor_id)
        if doctor is None:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = FollowDoctorSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            follower_service = FollowerService()

            try:
                followed = follower_service.unfollow_doctor(user, doctor)
                return Response({'message': 'Unfollowed'}, status=status.HTTP_200_OK)
            except Follower.DoesNotExist:
                follower_service.follow_doctor(user, doctor)
                return Response({'message': 'Followed'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class DoctorFollowersListView(APIView):
    def get(self, request):
        if request.user.is_doctor:  # Check if the logged-in user is a doctor
            followers_service = FollowersService()
            doctor_followers = followers_service.get_followers_of_doctor(request.user)
            return Response({'followers': [follower.name for follower in doctor_followers]}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)



class UserFollowedDoctorsListView(APIView):
    def get(self, request):
            followers_service = FollowersService()
            user_followed_doctors = followers_service.get_doctors_followed_by_user(request.user)
            serializer = DoctorAccountSerializer(user_followed_doctors,many=True)
            return Response({'followed_doctors': serializer.data}, status=status.HTTP_200_OK)
 
        
class DoctorList(APIView):
    def get(self, request, *args, **kwargs):
        doctors = DoctorService.get_all_doctors(self)
        serializer = DoctorAccountSerializer(doctors, many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class DoctorDetail(APIView):
    def get(self, request, doctor_id):
        doctor_service = DoctorService()
        doctor = doctor_service.get_doctor_by_id(doctor_id)
        if doctor:
            serializer = DoctorAccountSerializer(doctor)
            follows_doctor = Follower.objects.filter(user=request.user, doctor=doctor).exists()
            serialized_data = {"doctor": serializer.data, "follow": follows_doctor}
            return Response(serialized_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)
    
class UserChatListView(APIView):
    def get(self, request):
        user_id = request.user.id
        user_data = User.objects.all()
        chat_service_url = f"http://chatservice:8004/api/user_chats/{user_id}"
        try:
            response = requests.get(chat_service_url)
            chat_partners_data = response.json()
            chat_partners_ids = [partner['id'] for partner in chat_partners_data]
            chat_partners = user_data.filter(id__in=chat_partners_ids)
            serialized_chat_partners = []
            for partner, partner_data in zip(chat_partners, chat_partners_data):
                serialized_data = UserAccountSerializer(partner).data
                serialized_data['chat_id'] = partner_data['id']
                serialized_chat_partners.append(serialized_data)
            return Response({'chat_partners': serialized_chat_partners}, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            return Response({'error': 'Error connecting to the Chat service'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetDoctorGraduations(APIView):
    def get(self, request, doctor_id):
        graduations = DoctorGraduation.objects.filter(user_id=doctor_id)
        serializer = DoctorGraduationSerializer(graduations, many=True)
        return Response(serializer.data)

class GetAllLanguages(APIView):
    def get(self, request):
        languages = Language.objects.all()
        serializer = LanguageSerializer(languages, many=True)
        return Response(serializer.data)

class GetUsersByLanguage(APIView):
    def get(self, request, language_id):
        users = UserAccount.objects.filter(doctorlanguage__language_id=language_id)
        serializer = DoctorAccountSerializer(users, many=True)
        return Response(serializer.data)

class GetAllSpecializing(APIView):
    def get(self, request):
        specializations = Specializing.objects.all()
        serializer = SpecializingSerializer(specializations, many=True)
        return Response(serializer.data)

class GetUsersBySpecializing(APIView):
    def get(self, request, specializing_id):
        users = UserAccount.objects.filter(specializations__specializing_id=specializing_id)
        serializer = DoctorAccountSerializer(users, many=True)
        return Response(serializer.data)