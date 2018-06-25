"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest, Http404
from django.template import RequestContext
from datetime import datetime
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.http import require_http_methods

#from django.views.decorators.cache import never_cache, cache_page
from .models import *
from .forms import *


def pages(request, slug):
    try:
        page = Page.objects.get(slug=slug)
    except:
        raise Http404("Страница не найдена")
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/page.html',
        {
            'page':page,
        }
    )

def home(request):
    """Renders the home page."""
    try:
        page = HomePage.objects.get(pk=1).page
    except:
        raise Http404("Страница не найдена")
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/page.html',
        {
            'page':page,
        }
    )

@require_http_methods(['POST'])
def feedback(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    form = FeedbackForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        if request.is_ajax():
            return HttpResponse()
        else:
            return redirect('index')
    return render(request, 'app/form.html', {'form': form})
