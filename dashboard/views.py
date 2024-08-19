from django.views import generic
from .models import Comment


class CommentsListView(generic.ListView):
    model = Comment
    template_name = "dashboard/comments_list.html"
    context_object_name = "comments"
    paginate_by = 25

    def get_queryset(self):
        return Comment.objects.filter(parent__isnull=True)


class CommentDetailView(generic.DetailView):
    model = Comment
    template_name = "dashboard/comment_replies.html"
    context_object_name = "comment"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["replies"] = self.object.replies.all()
        return context
