from rest_framework import routers
from django.urls import path

from accounts.api.login_api import LoginApi

urlpatterns = [
    path('login/', LoginApi.as_view()),
]

router = routers.SimpleRouter()
