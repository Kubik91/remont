"""
Definition of views.
"""

from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, Http404
from django.template import RequestContext
from datetime import datetime
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from sekizai.helpers import get_varname
from django.contrib.auth.models import User
from django.core.mail import send_mail
import threading

from .models import *
from .forms import *


def pages(request, slug = False):
    if slug:
        page = get_object_or_404(Page, slug=slug)
    else:
        page = get_object_or_404(Page.objects.filter(homePage__isnull=False))
    if page.view:
        page.view = 'app/temp/' + page.view
        if page.layout:
            return render(
                request,
                'app/view.html',
                {
                    'page': page,
                }
            )
        else:
            return render(
                request,
                page.view,
                {
                    'page': page,
                }
            )
    return render(
        request,
        'app/page.html',
        {
            'page':page,
        }
    )

def sendMail(user, feedback, request):
    if user.email:
        message = '<div>Заявка №'+str(feedback.pk)+':</br>/n'\
            +'<p>Имя: '+feedback.name+'</p>'\
            +'<p>Телефон: '+str(feedback.phone)+'</p>'\
            +'<p>Содержание: '+feedback.text+'</p>'\
            +'<p><img href="http://iteh.by/media/'+str(feedback.image)+'"></p>'\
            +'<p>Создана:'+str(feedback.created_at)+'</p>'\
            +'</div>'
        send_mail(
            'Заявка с сайта '+request.get_host(),
            message,
            'webmaster@iteh.by',
            [user.email],
            fail_silently=True
        )

@require_http_methods(['POST'])
def feedback(request):
    assert isinstance(request, HttpRequest)
    form = FeedbackForm(request.POST, request.FILES)
    if form.is_valid():
        new_feedback = form.save()
        users = User.objects.all()
        for user in users:
            my_thread = threading.Thread(target=sendMail, args=(user, new_feedback, request))
            my_thread.start()
        if request.is_ajax():
            return HttpResponse()
        else:
            return redirect('index')
    return render(request, 'app/form.html', {'form': form})
