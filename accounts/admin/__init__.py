from django.contrib import admin
from rest_framework.authtoken.models import TokenProxy

from accounts.admin.token_admin import FilterTokenAdmin
from accounts.admin.user_admin import UserAdmin
from accounts.models import User

admin.site.register(User, UserAdmin)


admin.site.unregister(TokenProxy)
admin.site.register(TokenProxy, FilterTokenAdmin)