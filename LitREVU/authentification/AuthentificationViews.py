from django.shortcuts import render, redirect
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View
from . import forms


@requires_csrf_token
def custom_csrf_failure(request, reason=""):
    """
    Custom CSRF failure view.
    This function renders a custom HTML template for CSRF failure.
    """
    return render(request, 'custom_csrf_failure.html', {'reason': reason})


def home(request):
    return render(request, 'authentification/home.html')


class LoginView(View):
    template_name = 'authentication/login.html'
    form_class = forms.LoginForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                # Check if the 'next' parameter exists in the request
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)  # Redirect to the next URL if provided
                else:
                    return redirect('home_review')  # Redirect to home_review if no next URL provided
        message = 'Identifiants invalides.'
        return render(request, self.template_name, context={'form': form, 'message': message})


class SignupView(View):
    template_name = 'authentication/signup.html'
    form_class = forms.SignupForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('ticket')
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    template_name = 'authentication/logout.html'

    def get(self, request):
        logout(request)
        return redirect('home')
