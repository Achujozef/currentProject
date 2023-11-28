from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserAccountCreateView.as_view(), name='user-register'),
    path('user-documents/', UserDocumentListView.as_view(), name='user-document-list'),
    path('user-documents/create/', UserDocumentCreateView.as_view(), name='user-document-create'),
    path('user-documents/<int:pk>/', UserDocumentRetrieveView.as_view(), name='user-document-retrieve'),
    path('user-documents/update/<int:pk>/', UserDocumentUpdateView.as_view(), name='user-document-update'),
    path('user-documents/delete/<int:pk>/', UserDocumentDestroyView.as_view(), name='user-document-destroy'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('change-phone-number/', ChangePhoneNumberView.as_view(), name='change-phone-number'),
    path('change-photo/', ChangePhotoView.as_view(), name='change-photo'),
    path('follow-doctor/<int:doctor_id>/', FollowDoctorView.as_view(), name='follow-doctor'),
    path('doctor-followers/', DoctorFollowersListView.as_view(), name='doctor-followers-list'),
    path('user-followed-doctors/', UserFollowedDoctorsListView.as_view(), name='user-followed-doctors-list'),
    path('user/', GetUser.as_view()),
    path('users-edit/', EditUserProfileView.as_view(), name='edit_user_profile'),
    path('doctors/', DoctorList.as_view(), name='doctor-list'),
    path('doctor/<int:doctor_id>/', DoctorDetail.as_view(), name='doctor-detail'),
    path('chatList/', UserChatListView.as_view(), name='UserChatListView'),
    
    path('doctor-graduations/<int:doctor_id>/', GetDoctorGraduations.as_view(), name='get_doctor_graduations'),
    path('languages/', GetAllLanguages.as_view(), name='get_all_languages'),
    path('users-by-language/<int:language_id>/', GetUsersByLanguage.as_view(), name='get_users_by_language'),
    path('specializing/', GetAllSpecializing.as_view(), name='get_all_specializing'),
    path('users-by-specializing/<int:specializing_id>/', GetUsersBySpecializing.as_view(), name='get_users_by_specializing'),

]