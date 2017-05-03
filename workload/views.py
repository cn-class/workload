#-*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User
from django.db.models import Count,Sum
from .excel_utils import WriteToExcel,WriteToExcelManager

from django.utils.timezone import datetime

from .models import Teaching
from .forms import TeachingForm ,ChosenForm

# Create your views here.
@login_required
def workload_list(request,id=None):

	current_user = request.user
	if request.user.is_staff or request.user.is_superuser:
		return redirect("workload:report")

	else:
		queryset = Teaching.objects.filter(user=current_user,date__year=datetime.today().year)
		if request.method == "POST":
			form = ChosenForm(request.POST or None)
			date = request.POST.get("year")
			d = datetime.strptime(date,"%Y-%m-%d")
			queryset = Teaching.objects.filter(user=current_user,date__year=d.year)
		else:
			form = ChosenForm()
	
	context = {
		# "form": form,
		"form" : form,
		"object_list": queryset,
		"current_user":current_user,
	}
	return render(request,"workload/workload_list.html",context)

	
@login_required
def workload_create(request):
	current_user = request.user
	if request.method == "POST":
		form = TeachingForm(request.POST or None, initial={'user':current_user,})
		if form.is_valid():
			print("success")
			instance = form.save(commit=False)
			instance.user = current_user
			instance.save()
			messages.success(request,"Successfully Created")
			return redirect("workload:list")
		else:
			print(form)
			messages.error(request, "Not Successfully Created")
	else:
		form = TeachingForm()

	context = {
		"form": form,
		"current_user":current_user,
	}
	return render(request, "workload_form.html", context)


@login_required
def workload_update(request, id=None):
	instance = get_object_or_404(Teaching,id=id)
	form = TeachingForm(request.POST or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = instance.user
		instance.save()
		messages.success(request,"<a href='#'>Saved</a>",extra_tags='html_safe')
		return redirect("workload:list")
	else:
		print("2")

	context = {
		"form": form,
		"instance" : instance,
	}
	return render(request, "workload_form.html", context)

	
@login_required
def workload_delete(request, id=None):
	instance = get_object_or_404(Teaching,id=id)
	instance.delete()
	messages.success(request,"Successfully Deleted")
	return redirect("workload:list")


@login_required
def workload_export(request, id=None):
	current_user = request.user
	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
	if request.user.is_staff or request.user.is_superuser:
		queryset = Teaching.objects.all().filter(date__year=datetime.today().year)
		xlsx_data = WriteToExcelManager(queryset,current_user)
		response.write(xlsx_data)
	else:
		queryset = Teaching.objects.filter(user=current_user,date__year=datetime.today().year)
		xlsx_data = WriteToExcel(queryset,current_user)
		response.write(xlsx_data)

	return response


@login_required
def detail(request):
	return render(request, "workload/detail.html")


@login_required
def sum_detail(request):
	data = Teaching.objects.all().values('user__username').annotate(sum_items=Sum('num_of_lecture'))
	return JsonResponse(list(data), safe=False)


@login_required
def workload_report(request):
	current_user = request.user
	if not request.user.is_staff:
		return redirect("404.html")
	else:
		queryset = Teaching.objects.filter(user=current_user,date__year=datetime.today().year)
		if request.method == "POST":
			form = ChosenForm(request.POST or None)
			date = request.POST.get("year")
			d = datetime.strptime(date,"%Y-%m-%d")
			year = d.year
			# queryset = Teaching.objects.filter(user=current_user,date__year=d.year)
		else:
			form = ChosenForm()
			year = datetime.today().year

	print(year)
	context ={
		"year" : year ,
		"form" : form,
		"current_user":current_user,
	}
	return render(request, "workload/workload_report.html",context)


@login_required
def sum_report(request):
	data = Teaching.objects.filter(date__year=datetime.today().year).values('user__username').annotate(sum_items=Sum('num_of_lecture'))	
	# data = Teaching.objects.filter(date__year=y).values('user__username').annotate(sum_items=Sum('num_of_lecture'))
	# data = Teaching.objects.all().values('user__username','num_of_lecture','subject')
	for instance in data:
   		print(instance)

	return JsonResponse(list(data), safe=False)

