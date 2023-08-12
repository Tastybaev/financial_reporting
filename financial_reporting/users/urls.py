from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUp.as_view(template_name='users/account/signup.html'), name='signup'),
    path(
        'logout/',
        LogoutView.as_view(template_name='users/account/logged_out.html'),
        name='logout'
    ),
    path(
        'login/',
        LoginView.as_view(template_name='users/account/login.html'),
        name='login'
    ),
    path(
        'login_or_signup/',
        LoginView.as_view(template_name='users/account/login_or_signup.html'),
        name='login_or_signup'
    ),
    path(
        'password_change_form/',
        LoginView.as_view(template_name='users/account/password_change_form.html'),
        name='password_change_form'
    ),
    path(
        'password_change_done/',
        LoginView.as_view(template_name='users/account/password_change_done.html'),
        name='password_change_done'
    ),
    path(
        'password_reset_complete/',
        LoginView.as_view(template_name='users/account/password_reset_complete.html'),
        name='password_reset_complete'
    ),
    path(
        'password_reset_form/',
        LoginView.as_view(template_name='users/account/password_reset_form.html'),
        name='password_reset_form'
    ),
    path(
        'password_reset_confirm/',
        LoginView.as_view(template_name='users/account/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'password_reset_done/',
        LoginView.as_view(template_name='users/account/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'pricing/',
        TemplateView.as_view(template_name='users/payment/pricing.html'),
        name='pricing'
    ),
    path(
        'settings/',
        views.update_profile, 
        name='settings'
    ),
    path(
        'settings/delete_category/<int:category_id>/', 
        views.delete_category, 
        name='delete_category'
    )
]
