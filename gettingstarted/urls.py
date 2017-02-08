from django.conf.urls import include, url

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from account.views import (login_view ,register_view,logout_view)


from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^workload/', include('workload.urls', namespace='workload')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', login_view, name='login'),
    url(r'^register/', register_view, name='register'),
    url(r'^logout/', logout_view, name='logout'),
]
