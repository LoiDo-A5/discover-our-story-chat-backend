from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone_number')
    list_filter = ('name', 'email')
    search_fields = ('name', 'email', 'phone_number')
    exclude = ('first_name', 'last_name',)
