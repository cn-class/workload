from django.conf.urls import url
from django.contrib import admin

from .views import (
	workload_list,
	workload_create,
	workload_update,
	workload_delete,
	workload_report,
	# workload_export,
	# workload_export_score,
	workload_ex,
	workload_ex2,
	detail,
	sum_report,
	)

urlpatterns = [ 

	url( r'^$', workload_list, name='list'),
	url( r'^create/$', workload_create,name='create'),
	url( r'^report/$', workload_report,name='report'),
	url( r'^detail/$', detail,name='detail'),
	# url( r'^export/$', workload_export,name='export'),
	# url( r'^exportscore/$', workload_export_score,name='exportscore'),
	url( r'^export/$',workload_ex,name='export'),
	url( r'^exportscore/$',workload_ex2,name='exportscore'),
	url( r'^(?P<id>\d+)/edit/$', workload_update, name='update'),
	url( r'^(?P<id>\d+)/delete/$', workload_delete, name='delete'),

	url( r'^api/report/$',sum_report,name='sum_report'),

]