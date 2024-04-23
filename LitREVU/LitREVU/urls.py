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
from django.urls import path, include
from authentication.AuthenticationViews import SignUpView, LogoutView, LoginView, home, custom_csrf_failure, contact
from review.ReviewViews import HomeReviewView, TicketView, ReviewView, FollowingView
from review.ReviewViews import PostsView
from django.conf import settings

if settings.DEBUG:
    import debug_toolbar


app_name = 'accounts'

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls, name="admin"),
    path('login/', LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('signup/', SignUpView.as_view(
         template_name='authentication/signup.html'),
         name="signup"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('home/', home, name="home"),
    path('failure/', custom_csrf_failure, name="failure"),
    path('accounts/review/home_review/', HomeReviewView.as_view(), name='home_review'),
    path('accounts/review/posts/', PostsView.as_view(), name='posts'),
    path('create_ticket/', TicketView.create_ticket, name='create_ticket'),
    path('review/add_review/', ReviewView.as_view(), name='add_review'),
    path('review/following/', FollowingView.as_view(), name='following'),
    path('authentication/contact-us/', contact, name='contact'),
    path('create_ticket_review/', ReviewView.create_ticket_review, name='create_ticket_review'),
]
