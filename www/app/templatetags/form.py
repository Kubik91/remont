from django import template
from django.conf import settings
from django.utils.html import mark_safe
from ..forms import *
from ..models import Footer

register = template.Library()


@register.inclusion_tag('app/form.html', takes_context=True)
def render_form(context):
    form = FeedbackForm()
    sezikai_ctx_var = getattr(settings, 'SEKIZAI_VARNAME', 'SEKIZAI_CONTENT_HOLDER')
    return {
        'form':form,
        sezikai_ctx_var: context[sezikai_ctx_var]
    }


@register.simple_tag
def footer_addr():
    return Footer.objects.last().address


@register.simple_tag
def footer_middle():
    return Footer.objects.last().middle


@register.simple_tag
def footer_links():
    links = []
    for page in Footer.objects.last().pages.all():
        links.append(f'<li><a href="{page.get_absolute_url}">{page.title}</a></li>')
    return mark_safe(''.join(links))
