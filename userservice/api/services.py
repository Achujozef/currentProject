from .models import *

class ChangePasswordService:
    def change_password(self, user, new_password):
        user.set_password(new_password)
        user.save()


class ChangePhoneNumberService:
    def change_phone_number(self, user, new_phone_number):
        user.phonenumber = new_phone_number
        user.save()


class ChangePhotoService:
    def change_photo(self, user, new_photo):
        user.image = new_photo
        user.save()


class UserDocumentListService:
    def list_user_documents(self):
        return UserDocument.objects.all()


class UserDocumentCreateService:
    def create_user_document(self, data):
        user_document = UserDocument(**data)
        user_document.save()
        return user_document
    

class UserDocumentRetrieveService:
    def get_user_document(self, pk):
        try:
            return UserDocument.objects.get(pk=pk)
        except UserDocument.DoesNotExist:
            return None


class UserDocumentUpdateService:
    def update_user_document(self, user_document, data):
        for attr, value in data.items():
            setattr(user_document, attr, value)
        user_document.save()
        return user_document


class UserDocumentDeleteService:
    def delete_user_document(self, user_document):
        user_document.delete()


class DoctorService:
    def get_doctor_by_id(self, doctor_id):
        try:
            return UserAccount.objects.get(pk=doctor_id)
        except UserAccount.DoesNotExist:
            return None
        

class FollowerService:
    def follow_doctor(self, user, doctor):
        Follower.objects.create(user=user, doctor=doctor)

    def unfollow_doctor(self, user, doctor):
        Follower.objects.get(user=user, doctor=doctor).delete()


class FollowersService:
    def get_followers_of_doctor(self, doctor):
        followers = Follower.objects.filter(doctor=doctor).values('user')
        return UserAccount.objects.filter(pk__in=followers)

    def get_doctors_followed_by_user(self, user):
        doctors = Follower.objects.filter(user=user).values('doctor')
        return UserAccount.objects.filter(pk__in=doctors)

class DoctorService:
    def get_all_doctors(self):
        return (
            UserAccount.objects.filter(is_doctor=True)
            .prefetch_related('specializations', 'graduations')  # Use prefetch_related for reverse relations
        )

    def get_doctor_by_id(self, doctor_id):
        try:
            doctor = UserAccount.objects.get(id=doctor_id, is_doctor=True)
            return doctor
        except UserAccount.DoesNotExist:
            return None