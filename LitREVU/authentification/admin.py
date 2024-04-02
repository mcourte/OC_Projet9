from django.contrib import admin

from .models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "is_superuser",
        "is_staff",
        "is_active",
        "date_joined",
        "profile_photo",
    )


admin.site.register(User, UserAdmin)
