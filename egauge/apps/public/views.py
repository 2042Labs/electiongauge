from django.shortcuts import render_to_response
from django.template import RequestContext

def serve_download(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response["Access-Control-Allow-Origin"] = "*"
        return response
    return _wrapped_view_func

@serve_download
def homepage(request):
    return render_to_response(
        'homepage.html',
        {},
        context_instance=RequestContext(request)
        )

@serve_download
def state_predictions(request):
    return render_to_response(
        'state_predictions.html',
        {},
        context_instance=RequestContext(request)
        )
