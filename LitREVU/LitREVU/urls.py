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
from authentication.AuthenticationViews import SignUpView, LogoutView, LoginView, HomeView
from authentication.AuthenticationViews import custom_csrf_failure, ContactView
from review.ReviewViews import HomeReviewView, TicketView, ReviewView, FollowingView, UnfollowUserView
from review.ReviewViews import PostsView, TicketReviewView
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    import debug_toolbar

app_name = 'accounts'

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls, name="admin"),
    path('login/', LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('signup/', SignUpView.as_view(template_name='authentication/signup.html'), name="signup"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('', HomeView.as_view(), name="home"),
    path('failure/', custom_csrf_failure, name="failure"),
    path('accounts/review/home_review/', HomeReviewView.as_view(), name='home_review'),
    path('accounts/review/posts/', PostsView.as_view(), name='posts'),
    path('review/following/', FollowingView.as_view(), name='following'),
    path('authentication/contact_us/', ContactView.as_view(), name='contact'),
    path('authentication/update_profile/', ContactView.as_view(), name='update_profile'),
    path('unfollow/', UnfollowUserView.as_view(), name='unfollow_user'),
    path('review/create_ticket_review/', TicketReviewView.as_view(), name='create_ticket_review'),
    path('review/create_ticket/', TicketView.as_view(), name='create_ticket'),
    path('review/create_review/<int:ticket_id>/', ReviewView.as_view(), name='create_review'),
    path('review/edit_delete_review/<int:review_id>/', ReviewView.edit_delete_review, name='edit_delete_review'),
    path('review/edit_delete_ticket/<int:ticket_id>/', TicketView.edit_delete_ticket, name='edit_delete_ticket'),
    path('review/edit_ticket/<int:ticket_id>/', TicketView.edit_ticket, name='edit_ticket'),
    path('review/update_ticket/<int:ticket_id>/', TicketView.update_ticket, name='update_ticket'),
    path('review/update_review/<int:review_id>/', ReviewView.update_review, name='update_review'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
