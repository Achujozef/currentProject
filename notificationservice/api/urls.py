from django.urls import path
from .views import *

urlpatterns = [
    path('send-twlio-otp/', SendOtpTwlioMessages.as_view(), name='send_whatsapp_messages'),
    path('send-whatsapp-message/', SendWhatsAppMessageTwilio.as_view(), name='send-whatsapp-message'),
    path('send-otp/', SendOTPView.as_view({'post': 'create'})),
    path('notifications/<int:user_id>/', NotificationListCreateView.as_view(), name='notification-list-create'),
    path('delete-notification/<int:notification_id>/', NotificationDeleteView.as_view(), name='notification-detail'),
    path('clear-notifications/<int:user_id>/', NotificationClearView.as_view(), name='notification-clear'),

]