from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.
admin.site.register(UserAccount)
admin.site.register(UserDocument)
admin.site.register(Follower)

admin.site.register(Graduation)
admin.site.register(Language)
admin.site.register(Specializing)
admin.site.register(DoctorGraduation)
admin.site.register(DoctorLanguage)
admin.site.register(DoctorSpecializing)