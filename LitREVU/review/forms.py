from django import forms
from .models import Ticket, Review, TicketReview
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()


class TicketForm(forms.ModelForm):
    """ Formulaire pour la création et la modification d'un ticket."""
    title = forms.CharField(label="Titre", widget=forms.TextInput, required=True)
    description = forms.CharField(label="Description", widget=forms.Textarea, required=True)
    image = forms.FileField(label="Image", widget=forms.FileInput, required=True)

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    """Formulaire pour la création et la modification d'une critique."""
    headline = forms.CharField(label="Titre de la critique", widget=forms.TextInput(attrs={'id': 'headline'}),
                               required=True)
    rating = forms.IntegerField(
        label="Notation",
        widget=forms.HiddenInput(attrs={'id': 'rating'}),
        required=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    body = forms.CharField(label="Commentaire", widget=forms.Textarea(attrs={'id': 'body'}), required=True)

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]


class TicketReviewForm(forms.ModelForm):
    """Formulaire combiné pour la création d'un ticket et d'une critique associée."""
    # Champs pour le ticket
    title = forms.CharField(label="Titre", widget=forms.TextInput, required=True)
    description = forms.CharField(label="Description", widget=forms.Textarea, required=True)
    image = forms.FileField(label="Image", widget=forms.FileInput, required=True)

    # Champs pour la critique
    headline = forms.CharField(label="Titre de la critique", widget=forms.TextInput(attrs={'id': 'headline'}),
                               required=True)
    rating = forms.IntegerField(
        label="Notation",
        widget=forms.HiddenInput(attrs={'id': 'rating'}),
        required=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    body = forms.CharField(label="Commentaire", widget=forms.Textarea(attrs={'id': 'body'}), required=True)

    class Meta:
        model = TicketReview
        fields = ['title', 'description', 'image',  'headline', 'rating', 'body']


class FollowUsersForm(forms.ModelForm):
    """Formulaire pour suivre un utilisateur."""
    follows = forms.CharField(
        label="Nom d'utilisateur à suivre",
        max_length=128,
        widget=forms.TextInput(
            attrs={"placeholder": "Entrez le nom d'utilisateur à suivre"}
        ),
    )

    class Meta:
        model = User
        fields = ["follows"]

    def clean_follows(self):
        """Vérifie si l'utilisateur à suivre existe dans la base de données."""
        follows = self.cleaned_data["follows"]

        if not User.objects.filter(username=follows):
            raise forms.ValidationError(
                "Cet utilisateur n'est pas reconnu dans la base de donnée."
            )

        return follows
