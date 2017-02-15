from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User
from .excel_utils import WriteToExcel

from .models import Teaching
from .forms import TeachingForm,ExportForm
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
		if request.method == 'POST':
			form = ExportForm(data=request.POST)
	        # if form.is_valid():
	        #     user_id = form.data['user']
	        #     # user = Teaching.objects.get(pk=user_id)
	        #     user = Teaching.objects.filter(user=user_id)
	        if 'excel' in request.POST:
	            response = HttpResponse(content_type='application/vnd.ms-excel')
	            response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
	            xlsx_data = WriteToExcel(queryset,current_user)
	            response.write(xlsx_data)
	            return response

		else:
			form = ExportForm()
	
	context = {
		"form": form,
		"object_list": queryset,
		"current_user":current_user,
	}
	return render(request,"workload_list.html",context)
	

def workload_create(request):

	if not request.user.is_authenticated:
		return redirect("login")

	current_user = request.user
	form = TeachingForm(request.POST or None , initial={'user':current_user,})

	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = current_user
		instance.save()
		messages.success(request,"Successfully Created")
		return redirect("workload:list")
	else:
		messages.error(request, "Not Successfully Created")
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
	
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request,"<a href='#'>Saved</a>",extra_tags='html_safe')
		return redirect("workload:list")
	
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