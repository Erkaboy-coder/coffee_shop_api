from django.contrib import admin
from users.models import User

# @admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "role", "is_verified", "is_staff", "date_joined")
    search_fields = ("email", )
    list_filter = ("role", "is_verified", "is_staff")

admin.site.register(User, UserAdmin)