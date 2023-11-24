from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(AppointmentNotification)
admin.site.register(FollowNotification)
admin.site.register(PostNotification)
admin.site.register(Notification)