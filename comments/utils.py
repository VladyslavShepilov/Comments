from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.conf import settings
import jwt
import requests
from django.contrib.auth import get_user_model
from functools import wraps


def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        user = get_user_model().objects.get(id=user_id)
        return user
    except (
        jwt.ExpiredSignatureError,
        jwt.InvalidTokenError,
        get_user_model().DoesNotExist,
    ):
        return None


def get_new_tokens(refresh_token):
    response = requests.post(
        f"{settings.BASE_API_URL}{reverse('token_refresh')}",
        data={"refresh": refresh_token}
    )
    if response.status_code == 200:
        return response.json()
    return None


def jwt_required(view_func=None, login_url: str = "login"):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        redirect_to_login = HttpResponseRedirect(reverse(login_url))

        access_token = request.COOKIES.get("access_token")
        refresh_token = request.COOKIES.get("refresh_token")

        if not access_token:
            return redirect_to_login

        user = decode_jwt_token(access_token)
        if user is None:
            if refresh_token:
                new_tokens = get_new_tokens(refresh_token)
                if new_tokens:
                    access_token = new_tokens.get("access")
                    response = HttpResponseRedirect(request.path_info)
                    response.set_cookie("access_token", access_token, httponly=True)
                    request.user = decode_jwt_token(access_token)
                    return response
                else:
                    return redirect_to_login
            else:
                return redirect_to_login

        request.user = user
        return view_func(request, *args, **kwargs)

    return wrapper if view_func else lambda vf: jwt_required(vf, login_url=login_url)
