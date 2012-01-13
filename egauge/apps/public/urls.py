from django.conf.urls.defaults import *

urlpatterns = patterns('egauge.apps.public.views',
    (r'^', 'homepage'),
    (r'^state-predictions', 'state_predictions'),
)