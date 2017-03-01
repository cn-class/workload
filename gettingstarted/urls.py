from django.conf.urls import include, url

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from account.views import (login_view,register_view,logout_view)
from exporting.views import (all_towns,today_weather,weather_history,details)
from d3ex.views import (graph,play_count_by_month)


from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),

    #workload
    url(r'^workload/', include('workload.urls', namespace='workload')),

    #account
    url(r'^login/', login_view, name='login'),
    url(r'^register/', register_view, name='register'),
    url(r'^logout/', logout_view, name='logout'),

    #weather
    url(r'^weather/today/', today_weather, name='today_weather'),
    url(r'^weather/history/$', weather_history, name='weather_history'),
    url(r'^weather/details/(?P<weather_id>\w+)', details, name='details'),
    url(r'^towns/$', all_towns, name='towns'),

    url(r'^d3ex/',graph),
    url(r'^api/play_count_by_month',play_count_by_month, name='play_count_by_month'),
]
