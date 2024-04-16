from django.contrib import admin
from authentication.models import User
from review.models import Ticket, Review, UserFollows


class TicketInline(admin.TabularInline):
    model = Ticket


class ReviewInline(admin.TabularInline):
    model = Review


class UserFollowsInline(admin.TabularInline):
    model = UserFollows
    fk_name = 'user'


class UserAdmin(admin.ModelAdmin):
    inlines = [TicketInline, ReviewInline, UserFollowsInline]

    list_display = (
        "username",
        "is_superuser",
        "is_active",
        "date_joined",
    )


admin.site.register(User, UserAdmin)
