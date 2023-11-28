from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.core import exceptions
from .models import *
User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","name", "phonenumber", "email", "password")

    def validate(self, data):
        user = User(**data)
        password = data.get("password")

        try:
            validate_password(password, user)
        except exceptions.ValidationError as e:
            serializer_errors = serializers.as_serializer_error(e)
            raise exceptions.ValidationError(
                {"password": serializer_errors["non_field_errors"]}
            )
       
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            name=validated_data["name"],
            phonenumber=validated_data["phonenumber"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        return user

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = "__all__"

        
class UserDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocument
        fields = "__all__"

class FollowDoctorSerializer(serializers.Serializer):
    class Meta:
        model = Follower
        fields = "__all__"

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['name'] = user.name
        token['email'] = user.email
        token['phonenumber'] = user.phonenumber
        token['id'] = user.id
        token['is_doctor']= user.is_doctor

        token['image'] = "http://127.0.0.1:8001/api/users"+user.image.url if user.image else 'https://bootdey.com/img/Content/avatar/avatar7.png'
        return token


class SpecializingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specializing
        fields = "__all__"
    
class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"
class GraduationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Graduation
        fields = '__all__'

        
class DoctorGraduationSerializer(serializers.ModelSerializer):
    graduation = GraduationSerializer()
    class Meta:
        model = DoctorGraduation
        fields = "__all__"

class DoctorSpecializingSerializer(serializers.ModelSerializer):
    specializing = SpecializingSerializer()

    class Meta:
        model = DoctorSpecializing
        fields = '__all__'

class DoctorAccountSerializer(serializers.ModelSerializer):
    specializations = DoctorSpecializingSerializer(many=True, read_only=True)
    graduations = DoctorGraduationSerializer(many=True, read_only=True)

    class Meta:
        model = UserAccount
        fields = '__all__'