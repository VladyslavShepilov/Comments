from django.views import generic
from .models import Comment


class CommentsListView(generic.ListView):
    model = Comment
    template_name = "dashboard/comments_list.html"
    context_object_name = "comments"
    paginate_by = 25

    def get_queryset(self):
        return Comment.objects.filter(parent__isnull=True)
