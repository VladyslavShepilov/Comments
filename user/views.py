from django.views import generic
from .models import User


class UserDetailView(generic.DetailView):
    model = User
    template_name = "user/user_detail.html"
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_replies_count"] = self.object.comments.count()
        return context
