from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from authentification.models import User


class Ticket(models.Model):
    title = models.CharField(max_length=128, verbose_name="Titre")
    description = models.CharField(max_length=2048, blank=True, verbose_name="Description")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, verbose_name="Image")
    time_created = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128, verbose_name="Titre")
    body = models.CharField(max_length=8192, blank=True, verbose_name="Commentaires")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollowed(AbstractUser):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Following')
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Followed_by')
    groups = models.ManyToManyField(Group, related_name='Userfollowed_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='Userfollowed_permissions')

    class Meta:
        unique_together = ('user', 'followed_user')
