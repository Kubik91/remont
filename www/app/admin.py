# vim: set fileencoding=utf-8 :
from django.contrib import admin
from django.forms.utils import ErrorList
from jet.admin import CompactInline
from jet.filters import DateRangeFilter
from django.contrib.staticfiles.templatetags.staticfiles import static

from . import models


class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'phone',
        'text',
        'image',
        'created_at',
        'updated_at'
    )
    list_filter = (('created_at', DateRangeFilter), ('updated_at', DateRangeFilter), 'name')

class BlockAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'section',
        'text',
        'background',
        'button_url',
        'button_text',
        'animate',
    )
    list_filter = ('section',)
    class Media:
        css = {
            'all': (static('css/animate.min.css'),)
        }
        js = (
            static('admin/js/animate.js'),
            )


class CaruselItemAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'image',
        'text',
        'button_text',
        'button_url',
        'animate',
    )
    raw_id_fields = ('section',)
    search_fields = ('slug',)


class FilterCategoryAdmin(admin.ModelAdmin):

    list_display = ('id', 'title')


class FilterItemAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'image',
        'text',
        'button_text',
        'button_url',
        'pos',
        'width',
        'height',
    )
    raw_id_fields = ('categories', 'section')


class HomePageAdmin(admin.ModelAdmin):
    list_display = ('id', 'page')
    list_filter = ('page',)
    def has_add_permission(self, request):
        base_add_permission = super(HomePageAdmin, self).has_add_permission(request)
        if base_add_permission:
            # if there's already an entry, do not allow adding
            count = models.HomePage.objects.all().count()
            if count == 0:
                return True
        return False


class MapItemAdmin(admin.ModelAdmin):

    list_display = ('id', 'latitude', 'longitude', 'hint', 'baloon')
    raw_id_fields = ('section',)




class SectionImageAdmin(admin.ModelAdmin):

    list_display = ('id', 'section', 'image', 'position', 'animate')
    list_filter = ('section',)

class MaplItemInline(CompactInline):
    model = models.MapItem.section.through
    verbose_name = "Карта"
    verbose_name_plural = "Карты"
    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra

class CaruselItemInline(CompactInline):
    model = models.CaruselItem
    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra

class FilterItemInline(CompactInline):
    model = models.FilterItem
    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra

class BlockInline(CompactInline):
    model = models.Block
    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra

class TableInline(CompactInline):
    model = models.Table
    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra

class SectionImageInline(CompactInline):
    model = models.SectionImage
    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra


class SectionAdmin(admin.ModelAdmin):
    inlines = [
        SectionImageInline,
        TableInline,
        BlockInline,
        FilterItemInline,
        CaruselItemInline,
        MaplItemInline,
    ]
    list_display = (
        'id',
        'page',
        'title',
        'slug',
        'section_type',
        'display_title',
        'pos',
        'title_animate',
    )
    list_filter = ('page',)
    search_fields = ('slug',)
    class Media:
        js = (
            static('admin/js/section.js'),
            )

class SectionInline(CompactInline):
    model = models.Section
    extra = 0
    #def get_extra(self, request, obj=None, **kwargs):
    #    extra = 0
    #    return extra

class PageAdmin(admin.ModelAdmin):
    inlines = [
        SectionInline,
    ]
    list_display = (
        'id',
        'slug',
        'title',
        'body',
        'view',
        'status',
        'layout',
        'posmenu',
        'created_at',
        'updated_at',
    )
    list_filter = (('created_at', DateRangeFilter), ('updated_at', DateRangeFilter))
    search_fields = ('slug',)
    date_hierarchy = 'created_at'
    
class TableItemInline(CompactInline):
    model = models.TableItem
    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra

class TableAdmin(admin.ModelAdmin):
    inlines = [
        TableItemInline,
    ]
    list_display = ('id', 'title', 'section', 'pos', 'animate')
    raw_id_fields = ('section',)

    def has_add_permission(self, request):
        base_add_permission = super(TableAdmin, self).has_add_permission(request)
        if base_add_permission:
            count = models.Table.objects.all().count()
            if count < 2:
                return True
        return False

class TableItemAdmin(admin.ModelAdmin):

    list_display = ('id', 'row', 'col', 'value')
    raw_id_fields = ('table',)


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.Block, BlockAdmin)
_register(models.CaruselItem, CaruselItemAdmin)
_register(models.FilterCategory, FilterCategoryAdmin)
_register(models.FilterItem, FilterItemAdmin)
_register(models.HomePage, HomePageAdmin)
_register(models.MapItem, MapItemAdmin)
_register(models.Page, PageAdmin)
_register(models.SectionImage, SectionImageAdmin)
_register(models.Section, SectionAdmin)
_register(models.Table, TableAdmin)
_register(models.TableItem, TableItemAdmin)
_register(models.Feedback, FeedbackAdmin)
