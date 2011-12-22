from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^', include('egauge.apps.public.urls')),
)