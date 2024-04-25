from django.db.models.signals import post_save
from django.dispatch import receiver
from review.models import Ticket


@receiver(post_save, sender=Ticket)
def increment_user_ticket_number(sender, instance, created, **kwargs):
    """Fonction qui incrémente le numéro de ticket de l'utilisateur chaque fois qu'un nouveau ticket est créé.

    Args:
        sender: Le modèle qui envoie le signal (Ticket).
        instance: L'instance du modèle qui a déclenché le signal.
        created: Un drapeau indiquant si l'instance a été créée pour la première fois.
        **kwargs: Arguments supplémentaires."""
    if created:
        # Récupérer l'utilisateur associé au ticket
        user = instance.user
        # Récupérer le dernier numéro de ticket de l'utilisateur
        last_ticket_number = Ticket.objects.filter(user=user).order_by('-user_ticket_number').first()
        # Incrémenter le numéro de ticket de l'utilisateur
        new_ticket_number = 1 if last_ticket_number is None else last_ticket_number.user_ticket_number + 1
        # Mettre à jour le numéro de ticket de l'objet Ticket créé
        instance.user_ticket_number = new_ticket_number
        instance.save()
