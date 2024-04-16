"""
URL configuration for LitREVU project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from authentification.AuthentificationViews import SignUpView, LogoutView, LoginView, home, custom_csrf_failure
from review.ReviewViews import HomeReviewView


app_name = 'accounts'


urlpatterns = [
    # Define a path for the root URL
    path('admin/', admin.site.urls, name="admin"),
    path('login/', LoginView.as_view(
         template_name='authentification/login.html',
         redirect_authenticated_user=True),
         name="login"),
    path('signup/', SignUpView.as_view(
         template_name='authentification/signup.html'),
         name="signup"),
    path('logout/', LogoutView.as_view(
         template_name='authentification/logout.html'),
         name="logout"),
    path('home/', home, name="home"),
    path('failure/', custom_csrf_failure, name="failure"),
    path('home_review/', HomeReviewView.as_view(), name='home_review'),  # Update this line
]
