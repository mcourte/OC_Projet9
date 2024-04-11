from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


class Ticket(models.Model):

    title = models.CharField(max_length=128, name="title")
    description = models.CharField(
        max_length=2048, blank=True, name="description"
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    image = models.ImageField(null=True, blank=True, name="image")
    time_created = models.DateTimeField(auto_now_add=True)

    @property
    def has_review(self):
        if self.reviews.count() > 0:
            return True
        else:
            return False

    def __str__(self):
        """retourne la chaine de caractere du title"""
        return f"{self.title}"


class Review(models.Model):

    ticket = models.ForeignKey(
        to=Ticket, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="notation",
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    headline = models.CharField(max_length=128, verbose_name="title")
    body = models.CharField(
        max_length=8192, blank=True, verbose_name="comments"
    )
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """retourne la chaine de caractere du ticket"""
        return f"{self.ticket}"


class UserFollows(models.Model):
    """Modèle pour suivre les utilisateurs."""

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following",
    )

    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followed_by",
    )

    blocked = models.BooleanField(default=False)

    class Meta:
        """Options du modèle UserFollows."""

        # garantit qu'il n'y a pas d'instances UserFollows multiples pour les
        # paires unique
        unique_together = (
            "user",
            "followed_user",
        )

    def __str__(self):
        """Afficher les noms des users dans le shell"""
        return f"Utilisateur qui suit : {self.user.username} - Utilisateur suivi : {self.followed_user.username}"

    def unfollow(self):
        """Arrêter de suivre l'utilisateur suivi."""
        self.delete()

    def block(self):
        """Bloquer l'utilisateur suivi."""
        self.blocked = True
        self.save()
