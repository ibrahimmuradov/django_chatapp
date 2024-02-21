from .forms import UserEditForm, SecurityEditForm
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

Users = get_user_model()

def account_context_processor(request):
    context = {}

    if request.user.is_authenticated:
        # User profile settings
        if request.method == "POST" and "username" in request.POST:
            user_edit_form = UserEditForm(instance=request.user, data=request.POST, files=request.FILES, request=request)

            if user_edit_form.is_valid():
                user_edit_form.save()
        else:
            user_edit_form = UserEditForm(instance=request.user)

        context['user_form'] = user_edit_form

        # User security settings
        if request.method == "POST" and "email" in request.POST:
            security_edit_form = SecurityEditForm(instance=request.user, data=request.POST, request=request)

            if security_edit_form.is_valid():
                security_edit_form.save()
        else:
            security_edit_form = SecurityEditForm(instance=request.user)

        context['security_form'] = security_edit_form

    return context