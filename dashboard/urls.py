from django.urls import path
from .views import CommentsListView

urlpatterns = [
    path("comments/", CommentsListView.as_view(), name="comment-list"),
]
