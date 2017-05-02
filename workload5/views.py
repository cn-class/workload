#-*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User
from django.db.models import Count,Sum
from .excel_utils import WriteToExcel

from django.utils.timezone import datetime

from .models import Support
from .forms import SupportForm,ChosenForm

# Create your views here.
@login_required
def workload_list(request,id=None):

	current_user = request.user
	if request.user.is_staff or request.user.is_superuser:
		return redirect("workload5:report")

	else:
		queryset = Support.objects.filter(user=current_user,date__year=datetime.today().year)

		if request.method == "POST":
			form = ChosenForm(request.POST or None)
			date = request.POST.get("year")
			d = datetime.strptime(date,"%Y-%m-%d")
			queryset = Support.objects.filter(user=current_user,date__year=d.year)
		else:
			form = ChosenForm()
	
	context = {
		"form": form,
		"object_list": queryset,
		"current_user":current_user,
	}
	return render(request,"workload5/workload_list.html",context)

	

def workload_create(request):

	if not request.user.is_authenticated:
		return redirect("login")

	current_user = request.user

	if request.method == "POST":

		form = SupportForm(request.POST or None, initial={'user':current_user,})
		if form.is_valid():
			print("success")
			instance = form.save(commit=False)
			instance.user = current_user
			instance.save()
			messages.success(request,"Successfully Created")
			return redirect("workload5:list")
		else:
			print(form)
			messages.error(request, "Not Successfully Created")

	else:
		form = SupportForm()

	context = {
		"form": form,
		"current_user":current_user,
	}
	return render(request, "workload_form.html", context)



def workload_update(request, id=None):

	if not request.user.is_authenticated:
		return redirect("login")

	print("1")
	instance = get_object_or_404(Support,id=id)
	form = SupportForm(request.POST or None, instance=instance)
	print(form.errors)

	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = instance.user
		instance.save()
		messages.success(request,"<a href='#'>Saved</a>",extra_tags='html_safe')
		return redirect("workload5:list")
	
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

	instance = get_object_or_404(Support,id=id)
	instance.delete()
	messages.success(request,"Successfully Deleted")
	return redirect("workload5:list")



def workload_export(request, id=None):

	current_user = request.user
	if request.user.is_staff or request.user.is_superuser:
		queryset = Support.objects.all()
	else:
		queryset = Support.objects.filter(user=current_user)

	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
	xlsx_data = WriteToExcel(queryset,current_user)
	response.write(xlsx_data)
	print("excel")
	return response



def workload_report(request):

	if not request.user.is_authenticated :
		return redirect("login")

	if not request.user.is_staff:
		return render(request,"404.html")
	current_user = request.user
	context ={
		"current_user":current_user,
	}
	return render(request, "workload5/workload_report.html",context)



def detail(request):
	if not request.user.is_authenticated :
		return redirect("login")
	return render(request, "workload5/detail.html")



def sum_report(request):
	
	data = Support.objects.all().values('user__username').annotate(total=Sum('user'))
	for instance in data:
		print(instance)

	return JsonResponse(list(data), safe=False)

