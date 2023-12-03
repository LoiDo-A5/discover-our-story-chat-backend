from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'phone_number', 'first_name', 'last_name')
    list_filter = ('username', 'email')
    search_fields = ('username', 'email', 'phone_number')
