from django.urls import path
from .views import *

urlpatterns = [
    path('packeposts/', FeedsView.as_view(), name='feeds'),
    path('<int:post_id>/like-dislike/', LikeDislikePostView.as_view(), name='like_dislike_post'),
    path('posts/', ApiGatewayView.as_view(), name='api_gateway_posts'),
    path('posts/<int:post_id>/', ApiGatewayView.as_view(), name='api_gateway_delete_post'),
    path('posts/by-doctor/<int:doctor_id>/', ApiGatewayView.as_view(), name='list_posts_by_doctor'),

]