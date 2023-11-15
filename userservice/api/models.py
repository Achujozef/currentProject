from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self ,name, email,phonenumber, password=None):
        if not email:
            raise ValueError("User must have a email")
        if not phonenumber:
            raise ValueError("User must have a phone number")

        email = self.normalize_email(email)
        email  = email.lower()
        user = self.model(
            email = self.normalize_email(email),
            name  = name,
            phonenumber = phonenumber,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self ,name,phonenumber, email, password):
        user = self.create_user(
            email = email,
            name  = name,
            password = password,
            phonenumber = phonenumber,
        )
        user.is_doctor = True
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_verified = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class UserAccount(AbstractBaseUser):
    name = models.CharField(max_length = 50,blank=False)
    email  = models.EmailField(max_length = 100, unique = True,blank=False)
    phonenumber = models.CharField(max_length = 10,unique = True)
    image = models.ImageField(upload_to='profiles', blank=True,null=True)
    date_joined = models.DateField(auto_now_add = True)
    last_login = models.DateField(auto_now_add=True)
    
    is_doctor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_block = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phonenumber']

    objects = MyAccountManager()
    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
      return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

class UserDocument(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    document = models.FileField(upload_to='user_documents/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Follower(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE,related_name='followers')
    doctor = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='doctors_followed')
    def __str__(self):
        return f'{self.user.name} follows Dr {self.doctor.name}'
    