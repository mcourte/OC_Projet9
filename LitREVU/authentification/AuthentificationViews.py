from django.shortcuts import render, redirect
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth import login
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


@requires_csrf_token
def custom_csrf_failure(request, reason=""):
    """
    Custom CSRF failure view.
    This function renders a custom HTML template for CSRF failure.
    """
    return render(request, 'custom_csrf_failure.html', {'reason': reason})


def home(request):
    return render(request, 'authentification/home.html')


class LoginView(BaseLoginView):
    template_name = 'authentification/login.html'

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
            return redirect('home_review')  # Redirect to home_review if no next URL provided


class SignUpView(CreateView):
    template_name = 'authentification/signup.html'
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
