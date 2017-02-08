from django.conf.urls import url
from django.contrib import admin

from .views import (
	workload_list,
	workload_create,
	workload_detail,
	workload_update,
	workload_delete,
	workload_report,
	detail,
	)

urlpatterns = [ 

	url( r'^$', workload_list, name='list'),
	url( r'^(?P<id>\d+)/$', workload_detail, name='detail'),
	url( r'^create/$', workload_create,name='create'),
	url( r'^report/$', workload_report,name='report'),
	url( r'^detail/$', detail,name='detail'),
	url( r'^(?P<id>\d+)/edit/$', workload_update, name='update'),
	url( r'^(?P<id>\d+)/delete/$', workload_delete, name='delete'),
]