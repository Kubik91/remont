from django import template
from django.db.models import Max, Min
from unidecode import unidecode
from django.conf import settings
from django.template.defaultfilters import slugify
from sekizai.helpers import get_varname

import json

register = template.Library()

un = 0
stat_un = None

@register.inclusion_tag('app/block.html', takes_context=True)
def render_sec_block(context, section):
    if not hasattr(section, 'block'):
        return context
    sec_block = section.block
    image = None
    if hasattr(section, 'image'):
        image = section.image
    return {
        'sec_block':sec_block,
        'image':image,
        'section':section,
        get_varname(): context[get_varname()],
    }

@register.inclusion_tag('app/filter.html', takes_context=True)
def render_filter(context, section):
    if not hasattr(section, 'filter'):
        return context
    filter = section.filter.all()
    if filter.count() < 1:
        return
    categories = []
    for fil in filter:
        categories += fil.categories.all()
    categories = list(set(categories))
    return {
        'filter':filter,
        'categories':categories,
        get_varname(): context[get_varname()],
    }

@register.inclusion_tag('app/carusel.html', takes_context=True)
def render_carusel(context, section):
    if not hasattr(section, 'carusel'):
        return context
    carusel = section.carusel.all()
    if carusel.count() < 1:
        return
    return {
        'carusel':carusel,
        get_varname(): context[get_varname()],
    }


@register.inclusion_tag('app/map.html', takes_context=True)
def render_map(context, section):
    if not hasattr(section, 'map'):
        return context
    map = section.map.all()
    if map.count() < 1:
        return
    return {
        'map':map,
        get_varname(): context[get_varname()],
    }

@register.inclusion_tag('app/table.html', takes_context=True)
def render_table(context, section):
    if not hasattr(section, 'table'):
        return context
    tables = section.table.all()
    if tables.count() < 1:
        return
    image = None
    if not len(tables) > 1:
        if hasattr(section, 'image'):
            image = section.image
    return {
        'tables':tables,
        'image':image,
        'section':section,
        get_varname(): context[get_varname()],
    }


@register.filter
def min(queryset, field):
    return queryset.aggregate(min_value=Min(field)).get('min_value')

@register.filter
def max(queryset, field):
    return queryset.aggregate(max_value=Max(field)).get('max_value')

@register.filter
def getRange(end, start = 1):
    return range(int(start), end+1)

@register.filter
def getCell(queryset, args):
    args_dict = json.loads(args)
    col = args_dict['col']
    row = args_dict['row']
    return queryset.filter(col=col).filter(row=row)[0].value

@register.filter
def allCol(queryset, col):
    return queryset.filter(col=col)

@register.filter
def allRow(queryset, row):
    return queryset.filter(row=row)

@register.filter
def getValue(queryset):
    if not len(queryset):
        return ''
    return queryset[0].value

@register.filter
def length(queryset):
    return len(queryset)

@register.filter
def slug(value):
    return slugify(unidecode(value))

@register.filter
def uniq(value):
    global un
    un += 1
    return str(value)+'_'+str(un)

@register.filter
def reset_uniq(value):
    global un
    un = 0
    return ''

@register.filter
def stat_uniq(value):
    global stat_un
    if value:
        stat_un = value
    return stat_un