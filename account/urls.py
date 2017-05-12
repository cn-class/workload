from django.conf.urls import url,include
from django.contrib import admin

from django.contrib.auth import views as auth_views

from .views import (
	login_view,
	register_view,
	logout_view,
	settings,
	change_password,
	login_redirect,
	profile,
	edit_profile,
	)

urlpatterns = [ 

	url(r'^login/$', login_view, name='login'),
    url(r'^register/$', register_view, name='register'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),  # <--
    url(r'^settings/$', settings, name='settings'),
    url(r'^change-password/$', change_password, name='password'),
    url(r'^profile/$',profile ,name='profile'),
    url(r'^profile/edit/$',edit_profile ,name='edit_profile'),

]