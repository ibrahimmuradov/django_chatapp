from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .forms import UserLoginForm, PwdResetForm, PwdResetConfirmForm

app_name = 'account'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/auth-login.html',
                                                form_class=UserLoginForm,
                                                redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/account/login/'), name='logout'),
    path('register/', views.register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'),

    # password reset
    path('password-reset/', auth_views.PasswordResetView.as_view(
                                                            template_name='account/password-reset-form.html',
                                                            success_url='password-reset-email-confirm/',
                                                            email_template_name='account/password-reset-email.html',
                                                            form_class=PwdResetForm), name='pwd-reset'),

    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
                                                                template_name='account/password-reset-confirm.html',
                                                                success_url='/account/password-reset-complete/',
                                                                form_class=PwdResetConfirmForm),
                                                                name='password-reset-confirm'),

    path('password-reset/password-reset-email-confirm/', TemplateView.as_view(
                                                                            template_name='account/reset-status.html'),
                                                                            name='password-reset-done'),

    path('password-reset-complete/', TemplateView.as_view(template_name='account/reset-status.html'),
                                                          name='password-reset-complete'),

    path('change-password/', views.PasswordChangeView.as_view(template_name='account/password-change.html'),
                                                                name='change-password'),

    path('password-success/<slug:token>/', views.password_success, name='password-success'),

]