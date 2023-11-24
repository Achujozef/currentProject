from django.db import models

class Chat(models.Model):
    user_id = models.PositiveIntegerField()
    doctor_id = models.PositiveIntegerField()

    def __str__(self):
        return f"Chat between User {self.user_id} and Doctor {self.doctor_id}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=[('user', 'User'), ('doctor', 'Doctor')])
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_type} in {self.chat} at {self.timestamp}"

    class Meta:
        ordering = ('timestamp',)