from django.shortcuts import render_to_response
from django.template import RequestContext


def homepage(request):
    print 'Homepage is loading! Yay!'
    return render_to_response(
        'templates/homepage.html',
        {},
        context_instance=RequestContext(request)
        )