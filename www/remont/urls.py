"""
Definition of urls for remont.
"""

from django.conf.urls import url
from django.urls import path
import app.views
from django.conf.urls import include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
admin.autodiscover()

urlpatterns = [
    url(r'^$', app.views.pages, name='home'),
    path('feedback/', app.views.feedback, name='feedback'),

    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    url(r'^admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('<slug>', app.views.pages, name='pages')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                           document_root=settings.STATIC_ROOT)

