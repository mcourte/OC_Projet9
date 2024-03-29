from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username_validator = RegexValidator(
        regex=r'^[\w.@+-]+$',
        message=_("Le nom d'utilisateur doit contenir uniquement des caractères alphanumériques"),
        code='invalid_username'
    )

    password_validator = RegexValidator(
        regex=r'^(?=.*\d)(?=.*[!@#$%^&*()-_=+])[a-zA-Z0-9!@#$%^&*()-_=+]+$',
        message=_("Le mot de passe doit contenir entre 8 et 12 caractères avec au moins un caractère numérique"
                  " et un caractère spécial parmi ! @ # $ % ^ & * ( ) - _ = + "),
        code='invalid_password'
    )

    username = models.CharField(_("Nom d'utilisateur"), max_length=150, unique=True, validators=[username_validator],
                                error_messages={'unique': _("Un utilisateur avec ce nom d'utilisateur existe déjà.")})
    password = models.CharField(_("Mot de passe"), validators=[password_validator], max_length=12)
    email = models.EmailField(_("Adresse email"), unique=True, error_messages={'unique': _("Un utilisateur avec cette"
                                                                                           " adresse email"
                                                                                           " existe déjà.")})
    groups = models.ManyToManyField(Group, related_name='user_auth_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='user_auth_permissions')
    is_online = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
