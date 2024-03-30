from django import forms
from .models import Ticket
from django.contrib.auth import get_user_model

from . import models

User = get_user_model()


class TicketForm(forms.ModelForm):
    title = forms.CharField(label="Titre", widget=forms.TextInput)
    description = forms.CharField(label="Description", widget=forms.Textarea)
    image = forms.CharField(label="Image :")

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):

    rating = forms.IntegerField(
        label="Notation", widget=forms.HiddenInput(), required=True
    )
    body = forms.CharField(label="Commentaire", widget=forms.Textarea)
    headline = forms.CharField(label="Titre", widget=forms.TextInput)

    class Meta:
        model = models.Review
        fields = ["headline", "rating", "body"]


class FollowUsersForm(forms.ModelForm):
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
        follows = self.cleaned_data["follows"]

        if not User.objects.filter(username=follows):
            raise forms.ValidationError(
                "Cet utilisateur n'est pas reconnu dans la base de donnée."
            )

        return follows
