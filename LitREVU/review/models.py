from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.db.models import Q


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='ticket_images/', default='static/no-image.jpg')
    time_created = models.DateTimeField(auto_now_add=True)
    user_ticket_number = models.IntegerField(default=1)

    @property
    def has_review(self):
        return self.reviews.exists()

    def user_has_review(self, user):
        return self.reviews.filter(user=user).exists()

    def __str__(self):
        return self.title

    # Pour accéder à l'ID de l'instance de ticket
    def get_ticket_id(self):
        return self.id


class Review(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Notation")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128, verbose_name="Titre")
    body = models.CharField(max_length=8192, blank=True, verbose_name="Commentaires")
    time_created = models.DateTimeField(auto_now_add=True)
    responded = models.BooleanField(default=False)  # Champ indiquant si une réponse a été postée

    def __str__(self):
        return f"Review for {self.ticket.title}"

    def get_rating_range(self):
        return range(self.rating)

    def get_complement_range(self):
        return range(5 - self.rating)

    def has_user_already_reviewed(self):
        """
        Check if the user has already reviewed the ticket.
        """
        return Review.objects.filter(Q(user=self.user) & Q(ticket=self.ticket)).exists()


class TicketReview(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='ticket_reviews')


class UserFollows(models.Model):
    """Modèle pour représenter la relation de suivi entre les utilisateurs."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following")
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followed_by")
    blocked = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "followed_user")

    def count_followers(self):
        """Compte le nombre d'abonnés d'un utilisateur."""
        return UserFollows.objects.filter(followed_user=self.user).count()

    def count_following(self):
        """Compte le nombre d'utilisateurs suivis par un utilisateur."""
        return UserFollows.objects.filter(user=self.user).count()

    def unfollow(self):
        """Met fin à la relation de suivi entre les utilisateurs."""
        self.delete()

    @classmethod
    def is_following(cls, user, followed_user):
        """Vérifie si un utilisateur suit un autre utilisateur."""
        return cls.objects.filter(user=user, followed_user=followed_user).exists()
