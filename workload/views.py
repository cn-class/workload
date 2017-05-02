#-*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User
from django.db.models import Count,Sum
from .excel_utils import WriteToExcel

import datetime

from .models import Teaching
from .forms import TeachingForm ,ChosenForm

# Create your views here.
@login_required
def workload_list(request,id=None):

	current_user = request.user
	if request.user.is_staff or request.user.is_superuser:
		return redirect("workload:report")

	else:
		queryset = Teaching.objects.filter(user=current_user)

		if request.method == "POST":
			# if 'teaching_sub' in request.POST :
			# 	form = TeachingForm(request.POST or None, initial={'user':current_user,})
			# 	if form.is_valid():
			# 		print("success")
			# 		instance = form.save(commit=False)
			# 		instance.user = current_user
			# 		instance.save()
			# 		messages.success(request,"Successfully Created")
			# 		return redirect("workload:list")
			# 	else:
			# 		print("false")
			# 		messages.error(request, "Not Successfully Created")
			# 	form = TeachingForm()

			# if 'chosen_sub' in request.POST :
				form2 = ChosenForm(request.POST or None)
				year = request.POST.get("year")
				print(year)
				queryset = Teaching.objects.filter(date=year)
				# if form2.is_valid():
				# 	instance2 = form2.save(commit=False)
				# 	instance2.save()
				# 	messages.success(request,"Successfully Created")
				# 	return redirect("workload:list")
				# else:
				# 	messages.error(request, "Not Successfully Created")
				# form2 = ChosenForm()
			
		else:
			print("else")
			# form = TeachingForm()
			form2 = ChosenForm()
	
	context = {
		# "form": form,
		"form2" : form2,
		"object_list": queryset,
		"current_user":current_user,
	}
	return render(request,"workload/workload_list.html",context)

	

def workload_create(request):

	if not request.user.is_authenticated:
		return redirect("login")

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



def workload_update(request, id=None):

	if not request.user.is_authenticated:
		return redirect("login")

	instance = get_object_or_404(Teaching,id=id)
	form = TeachingForm(request.POST or None, instance=instance)
	print(form.errors)

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

	

def workload_delete(request, id=None):

	if not request.user.is_authenticated:
		return redirect("login")

	instance = get_object_or_404(Teaching,id=id)
	instance.delete()
	messages.success(request,"Successfully Deleted")
	return redirect("workload:list")



def workload_export(request, id=None):

		current_user = request.user
		if request.user.is_staff or request.user.is_superuser:
			queryset = Teaching.objects.all()
		else:
			queryset = Teaching.objects.filter(user=current_user)

		response = HttpResponse(content_type='application/vnd.ms-excel')
		response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
		xlsx_data = WriteToExcel(queryset,current_user)
		response.write(xlsx_data)
		print("excel")
		return response


def detail(request):
	if not request.user.is_authenticated :
		return redirect("login")

	return render(request, "workload/detail.html")


def sum_detail(request):
	data = Teaching.objects.all().values('user__username').annotate(sum_items=Sum('num_of_lecture'))
	return JsonResponse(list(data), safe=False)


def workload_report(request):

	if not request.user.is_authenticated :
		return redirect("login")

	if not request.user.is_staff:
		return redirect("404.html")
	current_user = request.user
	context ={
		"current_user":current_user,
	}
	return render(request, "workload/workload_report.html",context)


def sum_report(request):
	data = Teaching.objects.all().values('user__username').annotate(sum_items=Sum('num_of_lecture'))
	# data = Teaching.objects.all().values('user__username','num_of_lecture','subject')
	for instance in data:
   		print(instance)

   	# data = serializers.serialize("json",data)

	return JsonResponse(list(data), safe=False)

