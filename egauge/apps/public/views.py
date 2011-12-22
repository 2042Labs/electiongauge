from django.shortcuts import render_to_response

def homepage(request):
    print 'Homepage is loading! Yay!'
    return render_to_response('templates/choropleth/gingrich.html', {
      })