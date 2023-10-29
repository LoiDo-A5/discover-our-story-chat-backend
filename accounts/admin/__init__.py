from django.contrib import admin

from accounts.admin.user_admin import UserAdmin
from accounts.models import User

admin.site.register(User, UserAdmin)
