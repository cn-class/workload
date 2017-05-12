from django.conf.urls import url,include
from django.contrib import admin

from django.contrib.auth import views as auth_views

from .views import (
	login_view,
	register_view,
	logout_view,
	settings,
	password,
	login_redirect
	)

urlpatterns = [ 

	url(r'^login/', login_view, name='login'),
    url(r'^register/', register_view, name='register'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),  # <--
    url(r'^settings/', settings, name='settings'),
    url(r'^password/', password, name='password'),

]