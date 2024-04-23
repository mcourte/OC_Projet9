from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


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

    def __str__(self):
        return self.title

    # Pour accéder à l'ID de l'instance de ticket
    def get_ticket_id(self):
        return self.id


class Review(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="notation",
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128, verbose_name="title")
    body = models.CharField(max_length=8192, blank=True, verbose_name="comments")
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.ticket.title}"


class UserFollows(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following")
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followed_by")
    blocked = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "followed_user")

    def count_followers(self):
        return UserFollows.objects.filter(followed_user=self.user).count()

    def count_following(self):
        return UserFollows.objects.filter(user=self.user).count()

    def unfollow(self):
        self.delete()

    def block(self):
        self.blocked = True
        self.save()
