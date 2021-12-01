from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from .forms import RegistrationForm, UserEditForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from .admin import UserBase
from django.contrib.auth.models import AbstractBaseUser
from typing import Union
from .tokens import account_activation_token
# Create your views here.

@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    return render(request,
    'account/user/dashboard.html')

@login_required
def edit_details(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    
    return render(request,
                'account/user/edit_details.html', {'user_form': user_form})

@login_required
def delete_user(request: HttpRequest) -> HttpResponseRedirect:
    user: AbstractBaseUser = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')

# collects and saves the data when user press register button
def account_register(request: HttpRequest) -> HttpResponse:


    # if request.user.is_authenticated:
    #     return redirect('/')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            # take some of the data and saves it
            user: UserBase = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False # not active yet to log in
            user.save()
            # let's send him<an email
            current_site = get_current_site(request)
            subject: str = 'Activate your Account'
            message: str = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse('registered succesfully and activation sent')

    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})


def account_activate(request: HttpRequest, uidb64: str, token: str) -> Union[HttpResponse, HttpResponseRedirect]:
    # decode
    try:
        uidb: str = force_text(urlsafe_base64_decode(uidb64))
        user: AbstractBaseUser = UserBase.objects.get(pk=uidb)
        print("user for account activate is of type ", type(user))
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # redirect
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')
