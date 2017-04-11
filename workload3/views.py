#-*- coding: utf-8 -*-
from django.contrib import messages

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User
from django.db.models import Count,Sum
from .excel_utils import WriteToExcel

from .models import Research
from .forms import ResearchForm

# Create your views here.
def workload_list(request,id=None):

	if not request.user.is_authenticated:
		return redirect("login")

	current_user = request.user
	if request.user.is_staff or request.user.is_superuser:
		return redirect("workload3:report")

	else:
		queryset = Research.objects.filter(user=current_user)
		if request.method == "POST":
			form = ResearchForm(request.POST or None, initial={'user':current_user,})
			if form.is_valid():
				print("success")
				instance = form.save(commit=False)
				instance.user = current_user
				instance.save()
				messages.success(request,"Successfully Created")
				return redirect("workload3:list")
			else:
				messages.error(request, "Not Successfully Created")
		else:
			form = ResearchForm()
	
	context = {
		"form": form,
		"object_list": queryset,
		"current_user":current_user,
	}
	return render(request,"workload3/workload_list.html",context)

	

def workload_create(request):

	if not request.user.is_authenticated:
		return redirect("login")

	current_user = request.user

	if request.method == "POST":

		form = ResearchForm(request.POST or None, initial={'user':current_user,})
		if form.is_valid():
			print("success")
			instance = form.save(commit=False)
			instance.user = current_user
			instance.save()
			messages.success(request,"Successfully Created")
			return redirect("workload3:list")
		else:
			print(form)
			messages.error(request, "Not Successfully Created")

	else:
		form = ResearchForm()

	context = {
		"form": form,
		"current_user":current_user,
	}
	return render(request, "workload_form.html", context)



def workload_update(request, id=None):

	if not request.user.is_authenticated:
		return redirect("login")

	print("1")
	instance = get_object_or_404(Research,id=id)
	form = ResearchForm(request.POST or None, instance=instance)
	print(form.errors)

	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = instance.user
		instance.save()
		messages.success(request,"<a href='#'>Saved</a>",extra_tags='html_safe')
		return redirect("workload3:list")
	
	else:
		print("2")

	context = {
		"form": form,
		"instance" : instance,
	}
	return render(request, "workload_form.html", context)

	

def workload_delete(request, id=None):

	if not request.user.is_authenticated:
		return redirect("login")

	instance = get_object_or_404(Research,id=id)
	instance.delete()
	messages.success(request,"Successfully Deleted")
	return redirect("workload3:list")



def workload_export(request, id=None):
		
	current_user = request.user
	if request.user.is_staff or request.user.is_superuser:
		queryset = Research.objects.all()
	else:
		queryset = Research.objects.filter(user=current_user)

	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
	xlsx_data = WriteToExcel(queryset,current_user)
	response.write(xlsx_data)
	return response



def workload_report(request):

	if not request.user.is_authenticated :
		return redirect("login")

	if not request.user.is_staff:
		return redirect("404.html")
	current_user = request.user
	context ={
		"current_user":current_user,
	}
	return render(request, "workload3/workload_report.html",context)



def detail(request):
	if not request.user.is_authenticated :
		return redirect("login")
	return render(request, "workload3/detail.html")



def sum_report(request):
	data = Research.objects.all().values('user__username').annotate(total=Sum('user'))
	for instance in data:
		print(instance)

	return JsonResponse(list(data), safe=False)

