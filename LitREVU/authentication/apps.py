from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """Configuration de l'application d'authentification.
    Cette classe est responsable de la configuration de l'application d'authentification Django."""
    default_auto_field = "django.db.models.BigAutoField"
    name = "authentication"
