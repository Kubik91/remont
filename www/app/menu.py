from django.template.loader import get_template
from .models import *

def menu(request):
    pages = Page.objects.filter(status = 1)
    template = get_template('app/menu.html')
    html = template.render({'pages': pages})
    return {'menu': html}
