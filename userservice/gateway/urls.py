from django.urls import path
from .views import *

urlpatterns = [
    path('packeposts/', FeedsView.as_view(), name='feeds'),
    path('<int:post_id>/like-dislike/', LikeDislikePostView.as_view(), name='like_dislike_post'),
    path('posts/', ApiGatewayView.as_view(), name='api_gateway_posts'),
    path('posts/<int:post_id>/', ApiGatewayView.as_view(), name='api_gateway_delete_post'),
    path('posts/by-doctor/<int:doctor_id>/', ApiGatewayView.as_view(), name='list_posts_by_doctor'),
    path('notifications/', GetNotificationView.as_view(), name='list_posts_by_doctor'),
    path('clear-notifications/', ClearNotificationView.as_view(), name='list_posts_by_doctor'),
    path('delete-notification/<int:notification_id>/', DeleteNotificationView.as_view(), name='list_posts_by_doctor'),
    path('follower-post/', FollowerPostApiView.as_view(), name='follower-post'),
    path('book-slot/<int:slot_id>/', SlotBookingView.as_view(), name='book-slot'),
    path('list-slots/<int:doctor_id>/', GetSlotByDoctorView.as_view(), name='list-slots'),
    path('verify-payment/', VerifyPaymentView.as_view(), name='verify_payment'),
    path('create-comment/<int:post_id>/', PostCommentView.as_view(), name='list-slots'),
    path('comments/<int:post_id>/', GetCommentsView.as_view(), name='comment_list'),
]