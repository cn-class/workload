from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,

	)

from django.shortcuts import render,redirect

from .forms import UserLoginForm , UserRegisterForm

# Create your views here.

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
	return render(request, "form.html", {"form":form , "title":title})

def register_view(request):
	title = "Register"
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()

		new_user = authenticate(username=user.username,password=password)
		login(request, new_user)
		return redirect("workload:list")
	context = {
		"form":form,
		"title":title,
	}

	return render(request, "form.html", context)

def logout_view(request):
	logout(request)
	return redirect("login")


