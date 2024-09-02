from django.views import generic
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login
from django.shortcuts import redirect
from comments.utils import jwt_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
import requests
from django.conf import settings
from django.contrib.auth import get_user_model

from .forms import (
    UserRegistrationForm,
    UserUpdateForm,
    OptionalPasswordChangeForm
)


class UserRegisterView(generic.edit.CreateView):
    form_class = UserRegistrationForm
    template_name = "user/register.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response


class UserLoginView(LoginView):
    template_name = "user/login.html"
    success_url = reverse_lazy("comment-list")

    def form_valid(self, form):

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        response = requests.post(
            f"{settings.BASE_API_URL}{reverse('token_obtain_pair')}",
            data={"username": username, "password": password},
        )

        if response.status_code == 200:
            tokens = response.json()
            access_token = tokens.get("access")
            refresh_token = tokens.get("refresh")

            response = super().form_valid(form)

            response.set_cookie(
                "access_token", access_token, httponly=True, secure=True, path="/"
            )
            response.set_cookie(
                "refresh_token", refresh_token, httponly=True, secure=True, path="/"
            )
            return response
        else:
            return self.form_invalid(form)


class UserDetailView(generic.DetailView):
    model = get_user_model()
    template_name = "user/user_detail.html"
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_user"] = self.request.user
        context["user_replies_count"] = self.object.comments.count()
        return context


class UserUpdateView(generic.edit.FormView):
    template_name = "user/update.html"
    form_class = UserUpdateForm
    success_url = reverse_lazy("profile")

    def get(self, request, *args, **kwargs):
        user_form = UserUpdateForm(instance=request.user)
        password_form = OptionalPasswordChangeForm(user=request.user)
        return self.render_to_response(
            self.get_context_data(user_form=user_form, password_form=password_form)
        )

    @method_decorator(jwt_required)
    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        password_form = OptionalPasswordChangeForm(user=request.user, data=request.POST)

        context = self.get_context_data(
            user_form=user_form, password_form=password_form
        )

        if user_form.is_valid():
            user_form.save()

        password_provided = request.POST.get("new_password1") or request.POST.get(
            "new_password2"
        )
        if password_provided:
            if password_form.is_valid():
                password_form.save()
            else:
                context["password_errors"] = password_form.errors

        if not user_form.is_valid() or (
            password_provided and not password_form.is_valid()
        ):
            return redirect(self.get_success_url())

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("user-detail", kwargs={"pk": self.request.user.pk})
