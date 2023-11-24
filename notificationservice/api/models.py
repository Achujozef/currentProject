from django.db import models


class Notification(models.Model):
    CONTENT_TYPES = (
        ('post', 'Post'),
        ('follow', 'Follow'),
        ('appointment', 'Appointment'),
    )

    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES , default='')
    content = models.TextField()
    user_id= models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content_type} notification for user {self.user_id} at {self.created_at}"


class PostNotification(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    doctor_id = models.PositiveBigIntegerField()

class FollowNotification(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    followed_id = models.PositiveBigIntegerField()

class AppointmentNotification(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    appointment_id = models.PositiveBigIntegerField()
