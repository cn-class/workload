
from django.shortcuts import render,redirect,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import (authenticate,get_user_model,login,logout,)

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from social_django.models import UserSocialAuth
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .forms import UserLoginForm, RegistationForm, EditProfileForm


def login_redirect(request):
    return redirect('account:login')


def login_view(request):

    if request.user.is_authenticated:
        return redirect("workload:list")
        
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("workload:list")
    return render(request, "account/form.html", {"form":form , "title":title})


def register_view(request):
    if request.method == "POST":
        form = RegistationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("account:login")

    else:
        form = RegistationForm()

    context = {
        "form":form,
        "title": "Register",
    }
    return render(request,"account/form.html",context)
    

def logout_view(request):
    logout(request)
    return redirect("account:login")


@login_required
def settings(request):
    current_user = request.user
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    try:
        facebook_login = user.social_auth.get(provider='google')
    except UserSocialAuth.DoesNotExist:
        google_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'account/settings.html', {
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'google_login': google_login,
        'can_disconnect': can_disconnect,
        "current_user":current_user,
    })


@login_required
def change_password(request):

    current_user = request.user
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('account:settings')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'account/password.html', {'form': form,"current_user":current_user})


@login_required
def profile(request):
    current_user = request.user
    context = {
        "current_user":current_user,
    }
    return render(request,"account/profile.html",context)


@login_required
def edit_profile(request):
    current_user = request.user
    if request.method == "POST":
        form = EditProfileForm(request.POST,instance=current_user)

        if form.is_valid:
            form.save()
            return redirect("account:profile")

    else:
        form = EditProfileForm(instance=current_user)

    context = {
        "current_user":current_user,
        "form":form,
    }
    return render(request,"account/edit_profile.html",context)



def page_not_found(request):

    return render(request,"404.html")


# def server_error(request):
#     response = render_to_response('404.html',)
#     response.status_code = 500

#     return  response