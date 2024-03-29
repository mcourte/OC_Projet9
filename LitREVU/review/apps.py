from django.contrib import admin
from .models import Ticket, Review, UserFollows


class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "user")


class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ("followed_user_id", "user_id")


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review)
admin.site.register(UserFollows, UserFollowsAdmin)
