from django.views import generic
from django.db.models import Count

from .models import Comment
from .forms import CommentForm


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
        context["next_sort_order"] = "desc" if self.request.GET.get("sort_order", "asc") == "asc" else "asc"
        context["comment_form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        self.object_list = queryset
        context = self.get_context_data(object_list=queryset)

        form = CommentForm(request.POST)
        if form.is_valid():
            form.save(user=self.request.user)
            context["comment_form"] = CommentForm()
        else:
            context["comment_form"] = form

        return self.render_to_response(context)


class CommentDetailView(generic.DetailView):
    model = Comment
    template_name = "dashboard/comment_replies.html"
    context_object_name = "comment"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["replies"] = (
            self.object.replies
            .select_related("user")
            .annotate(reply_count=Count("replies"))
        )
        return context
