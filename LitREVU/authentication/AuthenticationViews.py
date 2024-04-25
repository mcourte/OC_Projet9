from django.shortcuts import render, redirect
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView as BaseLoginView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView
from django.views import View
from authentication.forms import ContactUsForm
from django.core.mail import send_mail


@requires_csrf_token
def custom_csrf_failure(request, reason=""):
    """Vue de gestion des échecs CSRF personnalisée.
    Cette fonction rend un modèle HTML personnalisé en cas d'échec CSRF."""
    return render(request, 'custom_csrf_failure.html', {'reason': reason})


class HomeView(View):
    """Vue pour afficher la page d'accueil du système."""
    def get(self, request):
        """Méthode pour gérer les requêtes GET."""
        return render(request, 'authentication/home.html')


class LoginView(BaseLoginView):
    """Vue pour gérer le processus de connexion des utilisateurs."""
    template_name = 'authentication/login.html'

    def get_context_data(self, **kwargs):
        """Récupère les données de contexte pour la vue de connexion."""
        context = super().get_context_data(**kwargs)
        # Passer le paramètre 'next' de la requête au contexte
        context['next'] = self.request.GET.get('next', '')
        return context

    def form_valid(self, form):
        """Méthode pour traiter un formulaire valide de connexion."""
        # Connexion de l'user
        self.user = form.get_user()
        login(self.request, self.user)

        # Vérifiez si le paramètre « next » existe dans la requête
        next_url = self.request.GET.get('next')
        if next_url:
            return redirect(next_url)
        else:
            return redirect('home_review')


class SignUpView(CreateView):
    """Vue pour gérer le processus d'inscription des utilisateurs."""
    template_name = 'authentication/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """Méthode pour traiter un formulaire valide d'inscription."""
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response

    def get_success_url(self):
        """Renvoie l'URL de redirection après une inscription réussie."""
        return reverse('home_review')


class LogoutView(TemplateView):
    """Vue pour gérer le processus de déconnexion des utilisateurs."""
    template_name = 'authentication/logout.html'

    def get(self, request, *args, **kwargs):
        """Méthode pour gérer les requêtes GET de déconnexion."""
        logout(request)
        return redirect('home')


class ContactView(View):
    """Vue pour gérer le formulaire de contact."""
    def get(self, request):
        """Méthode pour afficher le formulaire de contact."""
        form = ContactUsForm()
        return render(request, 'authentication/contact-us.html', {'form': form})

    def post(self, request):
        """Méthode pour traiter le formulaire de contact soumis."""
        form = ContactUsForm(request.POST)

        if form.is_valid():
            send_mail(
                subject=f'Message from {form.cleaned_data["name"]}',
                message=form.cleaned_data['message'],
                from_email=form.cleaned_data['email'],
                recipient_list=['courte.magali@gmail.com'],
            )
            return redirect('email-sent')  # Ajouter cette instruction de redirection

        return render(request, 'authentication/contact-us.html', {'form': form})
