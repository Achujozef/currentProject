from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.
admin.site.register(UserAccount)
admin.site.register(UserDocument)
admin.site.register(Follower)