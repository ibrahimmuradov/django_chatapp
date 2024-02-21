from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from .models import UserBase
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from services.generator import CodeGenerator
from django.urls import reverse_lazy


Users = get_user_model()


def register(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)

        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.email = register_form.cleaned_data['email']
            user.set_password(register_form.cleaned_data['password'])
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'ChatAPP - Activation Link'
            message = render_to_string('account/account-activation-email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)

            success = 'Your account has been created. \n To activate your account, verify your account using the activation link sent to your e-mail address.'

            return render(request, 'account/auth-register.html', {'data': success})

    else:
        register_form = UserRegisterForm()

    return render(request, 'account/auth-register.html', {'form': register_form})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        return redirect('/')
    else:
        return render(request, 'account/activation-invalid.html')


class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    login_url = 'account:login'

    def get_success_url(self):
        get_user = Users.objects.get(username=self.request.user.username)
        get_user.token_key = CodeGenerator.create_key(15, Users)
        get_user.save()

        return f'{reverse_lazy("account:password-success", kwargs={"token": get_user.token_key})}'


@login_required
def password_success(request, token):
    get_user = Users.objects.get(username=request.user.username)

    if token == get_user.token_key:
        get_user.token_key = None
        get_user.save()

        return render(request, 'account/password-change-success.html')
    else:
        return redirect('account:dashboard')
