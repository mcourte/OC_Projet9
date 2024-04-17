from django.shortcuts import render, redirect
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth import login
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from authentication.forms import ContactUsForm
from django.core.mail import send_mail


@requires_csrf_token
def custom_csrf_failure(request, reason=""):
    """
    Custom CSRF failure view.
    This function renders a custom HTML template for CSRF failure.
    """
    return render(request, 'custom_csrf_failure.html', {'reason': reason})


def home(request):
    return render(request, 'authentication/home.html')


class LoginView(BaseLoginView):
    template_name = 'authentication/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the 'next' parameter from the request to the context
        context['next'] = self.request.GET.get('next', '')
        return context

    def form_valid(self, form):
        # Log the user in
        self.user = form.get_user()
        login(self.request, self.user)

        # Check if the 'next' parameter exists in the request
        next_url = self.request.GET.get('next')
        if next_url:
            return redirect(next_url)  # Redirect to the next URL if provided
        else:
            return redirect(reverse_lazy('home'))  # Redirect to home if no next URL provided


class SignUpView(CreateView):
    template_name = 'authentication/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Register the user
        response = super().form_valid(form)
        # Log the user in after successful registration
        user = form.save()
        login(self.request, user)
        return response


class LogoutView(BaseLogoutView):
    def get_next_page(self):
        next_page = super().get_next_page()
        # Redirect to the home page after logout
        if next_page == reverse_lazy('login'):
            next_page = reverse_lazy('home')
        return next_page


def contact(request):
    if request.method == 'POST':
        # créer une instance de notre formulaire et le remplir avec les données POST
        form = ContactUsForm(request.POST)

        if form.is_valid():
            send_mail(
                     subject=f'Message from {form.cleaned_data["name"]}',
                     message=form.cleaned_data['message'],
                     from_email=form.cleaned_data['email'],
                     recipient_list=['courte.magali@gmail.com'],
                    )
            return redirect('email-sent')  # ajoutez cette instruction de retour
    # si le formulaire n'est pas valide, nous laissons l'exécution continuer jusqu'au return
    # ci-dessous et afficher à nouveau le formulaire (avec des erreurs).

    else:
        # ceci doit être une requête GET, donc créer un formulaire vide
        form = ContactUsForm()

    return render(request,
                  'authentication/contact-us.html',
                  {'form': form})
