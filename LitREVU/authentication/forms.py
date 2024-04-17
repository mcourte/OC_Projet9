from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d’utilisateur')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not username or not password:
            raise forms.ValidationError("Veuillez entrer à la fois votre nom d'utilisateur et votre mot de passe.")


class SignupForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        label='Email',
        help_text="Votre adresse email sera utilisée pour vous contacter.",
        error_messages={'required': 'Ce champ est obligatoire.'}
    )
    password1 = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(),
        help_text="Le mot de passe doit contenir au moins 8 caractères avec au moins un caractère numérique"
                  " et un caractère spécial.",
        error_messages={'required': 'Ce champ est obligatoire.'}
    )
    password2 = forms.CharField(
        label='Confirmation du mot de passe',
        widget=forms.PasswordInput(),
        help_text="Saisissez le même mot de passe que précédemment, pour vérification.",
        error_messages={'required': 'Ce champ est obligatoire.'}
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nom d\'utilisateur'
        self.fields['username'].error_messages['required'] = 'Ce champ est obligatoire.'

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ContactUsForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField()
    message = forms.CharField(max_length=1000)
