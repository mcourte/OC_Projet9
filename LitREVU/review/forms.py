from django import forms
from .models import Ticket, Review, TicketReview
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()


class TicketForm(forms.ModelForm):
    """ Formulaire pour la création et la modification d'un ticket."""
    title = forms.CharField(label="Titre", widget=forms.TextInput
                            (attrs={'placeholder': 'Titre du livre'}), required=True,
                            error_messages={'required': 'Veuillez saisir un titre.'})
    description = forms.CharField(label="Description", widget=forms.Textarea
                                  (attrs={'placeholder': 'Description de la demande'}), required=True,
                                  error_messages={'required': 'Veuillez saisir une description.'})
    image = forms.ImageField(
        label="Image",
        required=True,
        error_messages={'required': 'Veuillez sélectionner une image.'},
        widget=forms.ClearableFileInput(attrs={'aria-describedby': 'image-help-text'}),
        help_text="Veuillez sélectionner une image.",
    )
    image_description = forms.CharField(label="Description de l'image", required=False,
                                        widget=forms.Textarea(attrs={'placeholder': "Description de l'image"}))

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image_description'].widget.attrs['placeholder'] = "Description de l'image"


class ReviewForm(forms.ModelForm):
    """Formulaire pour la création et la modification d'une critique."""
    headline = forms.CharField(label="Titre de la critique", widget=forms.TextInput(attrs={'id': 'headline',
                               'placeholder': 'Titre de la critique'}),
                               required=True, error_messages={'required': 'Veuillez saisir un titre.'})
    rating = forms.IntegerField(
        label="Notation",
        widget=forms.HiddenInput(attrs={'id': 'rating'}),
        required=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    body = forms.CharField(label="Commentaire", widget=forms.Textarea(attrs={'id': 'body',
                           'placeholder': 'Votre commentaire'}), required=True,
                           error_messages={'required': 'Veuillez saisir une description.'})

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TicketReviewForm(forms.ModelForm):
    """Formulaire combiné pour la création d'un ticket et d'une critique associée."""
    # Champs pour le ticket
    title = forms.CharField(label="Titre", widget=forms.TextInput
                            (attrs={'placeholder': 'Titre du livre'}), required=True,
                            error_messages={'required': 'Veuillez saisir un titre.'})
    description = forms.CharField(label="Description", widget=forms.Textarea
                                  (attrs={'placeholder': 'Description de la demande'}), required=True,
                                  error_messages={'required': 'Veuillez saisir une description.'})
    image = forms.ImageField(
        label="Image",
        required=True,
        error_messages={'required': 'Veuillez sélectionner une image.'},
        widget=forms.ClearableFileInput(attrs={'aria-describedby': 'image-help-text'}),
        help_text="Veuillez sélectionner une image.",
    )
    image_description = forms.CharField(label="Description de l'image", required=False,
                                        widget=forms.Textarea(attrs={'placeholder': "Description de l'image"}))

    # Champs pour la critique
    headline = forms.CharField(label="Titre de la critique", widget=forms.TextInput(attrs={'id': 'headline',
                               'placeholder': 'Titre de la critique'}),
                               required=True, error_messages={'required': 'Veuillez saisir un titre.'})
    rating = forms.IntegerField(
        label="Notation",
        widget=forms.HiddenInput(attrs={'id': 'rating'}),
        required=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    body = forms.CharField(label="Commentaire", widget=forms.Textarea(attrs={'id': 'body',
                           'placeholder': 'Votre commentaire'}), required=True,
                           error_messages={'required': 'Veuillez saisir une description.'})

    class Meta:
        model = TicketReview
        fields = ['title', 'description', 'image',  'headline', 'rating', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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
