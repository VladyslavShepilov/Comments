from django.urls import path
from .views import CommentsListView, CommentFormView

urlpatterns = [
    path("", CommentsListView.as_view(), name="comment-list"),
    path("comment/add/", CommentFormView.as_view(), name="comment-form"),
]
