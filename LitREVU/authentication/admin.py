from django.contrib import admin
from authentication.models import User
from review.models import Ticket, Review, UserFollows


class TicketInline(admin.TabularInline):
    """Interface en ligne pour l'administration des tickets.
    Cette classe fournit une interface en ligne pour l'administration des tickets.
    Elle permet d'afficher et de gérer les tickets associés à d'autres modèles
    dans le panneau d'administration Django."""
    model = Ticket


class ReviewInline(admin.TabularInline):
    """Interface en ligne pour l'administration des critiques.
    Cette classe fournit une interface en ligne pour l'administration des critiques.
    Elle permet d'afficher et de gérer les critiques associées à d'autres modèles
    dans le panneau d'administration Django."""
    model = Review


class UserFollowsInline(admin.TabularInline):
    """Interface en ligne pour l'administration des suivis d'utilisateurs.
    Cette classe fournit une interface en ligne pour l'administration des suivis d'utilisateurs.
    Elle permet d'afficher et de gérer les relations de suivi entre les utilisateurs
    dans le panneau d'administration Django."""
    model = UserFollows
    fk_name = 'user'


class UserAdmin(admin.ModelAdmin):
    """Interface d'administration pour le modèle User.
    Cette classe fournit une interface d'administration pour gérer les utilisateurs
    dans le panneau d'administration Django.
    Elle affiche les utilisateurs avec leurs attributs principaux comme nom d'utilisateur, statut de superutilisateur,
    statut d'activation et date d'inscription.
    Permet également de gérer les tickets, les critiques et les suivis d'utilisateurs associés à chaque utilisateur."""
    inlines = [TicketInline, ReviewInline, UserFollowsInline]

    list_display = (
        "username",
        "is_superuser",
        "is_active",
        "date_joined",
    )


admin.site.register(User, UserAdmin)
