from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User

from .models import Teaching
from .forms import TeachingForm
# Create your views here.

def workload_list(request):

	if not request.user.is_authenticated:
		return redirect("login")
	current_user = request.user
	if request.user.is_staff or request.user.is_superuser:
		#queryset = Teaching.objects.all()
		return redirect("workload:report")
	else:
		queryset = Teaching.objects.filter(user=current_user)

	# queryset = Teaching.objects.all()
	context = {
		"object_list": queryset,
		"current_user":current_user,
	}
	return render(request,"workload_list.html",context)
	


def workload_detail(request, id=None ):

	if not request.user.is_authenticated:
		return redirect("login")

	instance = get_object_or_404(Teaching, id=id)
	context = {
		"title": instance.id,
		"instance":instance,
	}
	return render(request, "workload_detail.html",context)
	
def workload_create(request):

	if not request.user.is_authenticated:
		return redirect("login")

	form = TeachingForm(request.POST or None)
	
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request,"Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())
	else:
		messages.error(request, "Not Successfully Created")
	context = {
		"form": form,
	}
	return render(request, "workload_form.html", context)

def workload_update(request, id=None):

	if not request.user.is_authenticated:
		return redirect("login")

	instance = get_object_or_404(Teaching,id=id)
	form = TeachingForm(request.POST or None, instance=instance)
	
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request,"<a href='#'>Saved</a>",extra_tags='html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())
	
	context = {
		"form": form,
		"instance" : instance,
	}
	return render(request, "workload_form.html", context)
	

def workload_delete(request, id=None):

	if not request.user.is_authenticated:
		return redirect("login")

	instance = get_object_or_404(Teaching,id=id)
	instance.delete()
	messages.success(request,"Successfully Deleted")
	return redirect("workload:list")


def workload_report(request):

	if not request.user.is_authenticated :
		return redirect("login")

	return render(request, "workload_report.html")

	
def detail(request):

	if not request.user.is_authenticated :
		return redirect("login")

	return render(request, "detail.html")
