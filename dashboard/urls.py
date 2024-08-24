from django.urls import path
from .views import CommentsListView, CommentDetailView

urlpatterns = [
    path("", CommentsListView.as_view(), name="comment-list"),
    path("<int:pk>/replies/", CommentDetailView.as_view(), name="comment-replies"),
]
