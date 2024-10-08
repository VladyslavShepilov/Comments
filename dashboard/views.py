from django.views import generic
from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator

from .models import Comment
from .forms import CommentForm
from comments.utils import jwt_required
from django.conf import settings


class CommentsListView(generic.ListView):
    model = Comment
    template_name = "dashboard/comments_list.html"
    context_object_name = "comments"
    paginate_by = 25

    def get_queryset(self):
        queryset = (
            Comment.objects.filter(parent__isnull=True)
            .select_related("user")
            .prefetch_related("replies")
            .annotate(reply_count=Count("replies"))
        )
        print(settings.DEBUG)
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
        context["next_sort_order"] = (
            "desc" if self.request.GET.get("sort_order", "asc") == "asc" else "asc"
        )
        context["comment_form"] = CommentForm()
        context["current_query_params"] = self.request.GET.urlencode()
        return context

    @method_decorator(jwt_required)
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(user=self.request.user)

            print("Comment saved successfully with ID:", comment.id)

            return HttpResponseRedirect(
                f"{reverse('comment-list')}#comment-{comment.id}"
            )
        else:
            print("Form errors:", form.errors)
            parent_id = request.POST.get("parent")
            comment_identifier = (
                f"reply-form-{parent_id}" if parent_id else "comment-form"
            )

            context = self.get_context_data(object_list=self.get_queryset())
            context["comment_form"] = form
            context["fragment_identifier"] = comment_identifier

            return render(request, self.template_name, context, status=400)


class CommentFormView(generic.FormView):
    form_class = CommentForm
    template_name = "dashboard/comment_form.html"
    context_object_name = "comment_form"
    success_url = reverse_lazy("comment-list")

    @method_decorator(jwt_required)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.save(user=self.request.user)
            return super().form_valid(form)

        return HttpResponseRedirect(reverse("login"))
