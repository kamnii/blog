from django.urls import path
from posts.views import PostsView, DetailPostView, HashtagsView, PostCreateView

urlpatterns = [
    path('posts/<int:id>/', DetailPostView.as_view()),
    path('posts/create/', PostCreateView.as_view()),
    path('posts/', PostsView.as_view()),
    path('hashtags/', HashtagsView.as_view()),
]
