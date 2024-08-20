from django.views import generic
from django.db.models import Count

from .models import Comment


class CommentsListView(generic.ListView):
    model = Comment
    template_name = "dashboard/comments_list.html"
    context_object_name = "comments"
    paginate_by = 25

    def get_queryset(self):
        queryset = (
            Comment.objects.filter(parent__isnull=True)
            .select_related("user")
            .annotate(reply_count=Count("replies"))
        )

        sort_order = self.request.GET.get("sort_order", "asc")
        order_by = self.request.GET.get("order_by", "created_at")
        search_keys = ("username", "email", "created_at")

        if order_by in search_keys:
            if order_by in ("username", "email"):
                order_by = f"user__{order_by}"
            if sort_order == "desc":
                order_by = f"-{order_by}"
            queryset = queryset.order_by(order_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort_order = self.request.GET.get("sort_order", "asc")
        context["next_sort_order"] = "desc" if sort_order == "asc" else "asc"

        return context


class CommentDetailView(generic.DetailView):
    model = Comment
    template_name = "dashboard/comment_replies.html"
    context_object_name = "comment"

    def get_queryset(self):
        queryset = Comment.objects.select_related("user")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["replies"] = (
            self.object.replies.select_related("user").
            annotate(reply_count=Count("replies"))
        )
        return context
