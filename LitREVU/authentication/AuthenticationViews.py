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
    """
    Custom CSRF failure view.
    This function renders a custom HTML template for CSRF failure.
    """
    return render(request, 'custom_csrf_failure.html', {'reason': reason})


class HomeView(View):
    def get(self, request):
        return render(request, 'authentication/home.html')


class LoginView(BaseLoginView):
    template_name = 'authentication/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Passer le paramètre 'next' de la requête au contexte
        context['next'] = self.request.GET.get('next', '')
        return context

    def form_valid(self, form):
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
    template_name = 'authentication/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response

    def get_success_url(self):
        return reverse('home_review')


class LogoutView(TemplateView):
    template_name = 'authentication/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


class ContactView(View):
    def get(self, request):
        form = ContactUsForm()
        return render(request, 'authentication/contact-us.html', {'form': form})

    def post(self, request):
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
