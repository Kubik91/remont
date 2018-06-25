# vim: set fileencoding=utf-8 :
from django.contrib import admin
from django import forms
from django.forms.utils import ErrorList

from . import models

class HomePageModelForm(forms.ModelForm):
    def clean(self):
        if models.HomePage.objects.count() > 1:
            self._errors.setdefault('__all__', ErrorList()).append("Вы можете создать только одну домашнюю страницу.")
        return self.cleaned_data

#class TableModelForm(forms.ModelForm):
#    class Meta:
#        model = models.Table

#    def clean(self):
#        categories = self.cleaned_data.get('categories')
#        if categories and categories.count() > 3:
#            raise ValidationError('Maximum three categories are allowed.')

#        return self.cleaned_data

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


class CaruselItemAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'image',
        'text',
        'button_text',
        'button_url',
        'text_color',
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
        'position',
        'width',
        'height',
    )
    raw_id_fields = ('categories', 'section')


class HomePageAdmin(admin.ModelAdmin):
    form = HomePageModelForm
    list_display = ('id', 'page')
    list_filter = ('page',)


class MapItemAdmin(admin.ModelAdmin):

    list_display = ('id', 'latitude', 'longitude', 'hint', 'baloon')
    raw_id_fields = ('section',)




class SectionImageAdmin(admin.ModelAdmin):

    list_display = ('id', 'section', 'image', 'position', 'animate')
    list_filter = ('section',)

class SectionImageInline(admin.TabularInline):
    model = models.SectionImage
    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        #if obj:
            #return extra - obj.sections_set.count()
        return extra


class SectionAdmin(admin.ModelAdmin):
    inlines = [
        SectionImageInline,
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

class SectionInline(admin.TabularInline):
    model = models.Section
    inlines = [
        SectionImageInline,
    ]
    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        #if obj:
            #return extra - obj.sections_set.count()
        return extra

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
    list_filter = ('created_at', 'updated_at')
    search_fields = ('slug',)
    date_hierarchy = 'created_at'
    
class TableItemInline(admin.TabularInline):
    model = models.TableItem
    def get_extra(self, request, obj=None, **kwargs):
        extra = 0
        return extra

class TableAdmin(admin.ModelAdmin):
    inlines = [
        TableItemInline,
    ]
    list_display = ('id', 'title', 'section', 'position', 'animate')
    raw_id_fields = ('section',)

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
