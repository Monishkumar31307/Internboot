from django.urls import path
from . import views

app_name = 'likes'

urlpatterns = [
    path('toggle/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('my-likes/', views.liked_posts, name='liked_posts'),
]
