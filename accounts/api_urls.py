from rest_framework import routers
from django.urls import path

from accounts.api.login_api import LoginApi
from accounts.api.me import MeApi
from accounts.api.register_phone import RegisterPhoneApi

urlpatterns = [
    path('login/', LoginApi.as_view()),
    path('register/phone/', RegisterPhoneApi.as_view()),
    path('me/', MeApi.as_view()),
]

router = routers.SimpleRouter()
