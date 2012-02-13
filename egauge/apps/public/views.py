from django.shortcuts import render_to_response
from django.template import RequestContext

# TODO: Later this should be pulled from the database
ACTIVE = (
('romney', 'Mitt Romney'),
('gingrich', 'Newt Gingrich'),
('santorum', 'Rick Santorum'),
('paul', 'Ron Paul'),
)

# Note: This was an attempt as making the xml & js work
# cross site, but it didn't solve the issue.
# This should be deleted in the future. I just couldn't commit to it.
#def serve_download(view_func):
#    def _wrapped_view_func(request, *args, **kwargs):
#        response = view_func(request, *args, **kwargs)
#        response["Access-Control-Allow-Origin"] = "*"
#        return response
#    return _wrapped_view_func

#@serve_download
def homepage(request):
    return render_to_response('homepage.html',
        {
            'active_candidates': ACTIVE,
        },
        context_instance=RequestContext(request)
        )

#@serve_download
def state_predictions(request):
    return render_to_response(
        'state_predictions.html',
        {},
        context_instance=RequestContext(request)
        )
