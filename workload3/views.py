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

from .models import Research
from .forms import ResearchForm,ChosenForm

# Create your views here.
@login_required
def workload_list(request,id=None):
	current_user = request.user
	if request.user.is_staff or request.user.is_superuser:
		return redirect("workload3:report")
	else:
		queryset = Research.objects.filter(user=current_user,date__year=datetime.today().year)

		if request.method == "POST":
			form = ChosenForm(request.POST or None)
			date = request.POST.get("year")
			queryset = Research.objects.filter(user=current_user,date__year=date)
		else:
			form = ChosenForm()
	
	context = {
		"form": form,
		"object_list": queryset,
		"current_user":current_user,
	}
	return render(request,"workload3/workload_list.html",context)

	
@login_required
def workload_create(request):
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
		"head" : u"แบบฟอร์มงานวิจัย",
		"form": form,
		"current_user":current_user,
	}
	return render(request, "workload_form.html", context)


@login_required
def workload_update(request, id=None):
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
		"head" : u"แก้ไขแบบฟอร์มงานวิจัย",
		"form": form,
		"instance" : instance,
	}
	return render(request, "workload_form.html", context)

	
@login_required
def workload_delete(request, id=None):
	instance = get_object_or_404(Research,id=id)
	instance.delete()
	messages.success(request,"Successfully Deleted")
	return redirect("workload3:list")


@login_required
def workload_export(request, id=None):
	current_user = request.user
	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
	if request.user.is_staff or request.user.is_superuser:
		queryset = Research.objects.all().filter(date__year=datetime.today().year)
		xlsx_data = WriteToExcelManager(queryset,current_user)
		response.write(xlsx_data)
	else:
		queryset = Research.objects.filter(user=current_user,date__year=datetime.today().year)
		xlsx_data = WriteToExcel(queryset,current_user)
		response.write(xlsx_data)

	return response


@login_required
def workload_report(request):
	current_user = request.user
	if not request.user.is_staff:
		return redirect("404.html")
	else:
		queryset = Research.objects.filter(user=current_user,date__year=datetime.today().year)
		if request.method == "POST":
			form = ChosenForm(request.POST or None)
			date = request.POST.get("year")
			d = datetime.strptime(date,"%Y-%m-%d")
			year = d.year
			# queryset = Teaching.objects.filter(user=current_user,date__year=d.year)
		else:
			form = ChosenForm()
			year = datetime.today().year

	context ={
		"year" : year ,
		"form" : form,
		"current_user":current_user,
	}
	return render(request, "workload3/workload_report.html",context)


@login_required
def detail(request):
	return render(request, "workload3/detail.html")


@login_required
def sum_report(request):
	data = Research.objects.all().values('user__username').annotate(total=Count('user'))
	for instance in data:
		print(instance)

	return JsonResponse(list(data), safe=False)

