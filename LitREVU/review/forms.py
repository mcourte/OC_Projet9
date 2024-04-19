from django import forms
from .models import Ticket
from django.contrib.auth import get_user_model

from . import models

User = get_user_model()


class TicketForm(forms.ModelForm):
    title = forms.CharField(label="Titre", widget=forms.TextInput)
    description = forms.CharField(label="Description", widget=forms.Textarea)
    image = forms.ImageField(label="Image")
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class ReviewForm(forms.ModelForm):

    rating = forms.IntegerField(
        label="Notation", widget=forms.HiddenInput(), required=True
    )
    body = forms.CharField(label="Commentaire", widget=forms.Textarea)
    headline = forms.CharField(label="Titre", widget=forms.TextInput)
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Review
        fields = ["headline", "rating", "body"]


class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class TicketReviewForm(forms.ModelForm):
    # Champs pour le ticket
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField(required=False)

    # Champs pour la critique
    headline = forms.CharField(max_length=100)
    rating = forms.IntegerField(min_value=1, max_value=5)
    body = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image', 'headline', 'rating', 'body']


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
