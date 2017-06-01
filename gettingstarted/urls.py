from django.conf.urls import include, url

from django.conf import settings
from django.conf.urls import include, url, handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin

from account.views import login_redirect

from django.contrib import admin
admin.autodiscover()


# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),

    #workload
    url(r'^workload/', include('workload.urls', namespace='workload')),
    url(r'^thesis/', include('workload2.urls', namespace='workload2')),
    url(r'^research/', include('workload3.urls', namespace='workload3')),
    url(r'^document/', include('workload4.urls', namespace='workload4')),
    url(r'^support/', include('workload5.urls', namespace='workload5')),
    url(r'^position/', include('workload6.urls', namespace='workload6')),
    url(r'^benefit/', include('workload7.urls', namespace='workload7')),

    #account 
    url(r'^account/', include('account.urls', namespace='account')),
    url(r'^$',login_redirect,name='login_redirect'),

] 

handler404 = 'account.views.page_not_found'
handler500 = 'account.views.server_error'    
