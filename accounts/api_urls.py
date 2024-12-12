from rest_framework import routers
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.api.chatroom_list import ChatRoomList
from accounts.api.login_api import LoginApi
from accounts.api.me import MeApi
from accounts.api.message_list import ListMessage
from accounts.api.register_phone import RegisterPhoneApi

urlpatterns = [
    path('login/', LoginApi.as_view()),
    path('register/phone/', RegisterPhoneApi.as_view()),
    path('me/', MeApi.as_view()),
    path('rooms/', ChatRoomList.as_view(), name='rooms'),
    path('messages/', ListMessage.as_view(), name='messages'),
    path('token/refresh/', TokenRefreshView.as_view()),
]

router = routers.SimpleRouter()
