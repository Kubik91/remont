from django import template
from django.conf import settings
from ..forms import *

register = template.Library()

@register.inclusion_tag('app/form.html', takes_context=True)
def render_form(context):
    form = FeedbackForm()
    sezikai_ctx_var = getattr(settings, 'SEKIZAI_VARNAME', 'SEKIZAI_CONTENT_HOLDER')
    return {
        'form':form,
        sezikai_ctx_var: context[sezikai_ctx_var]
    }