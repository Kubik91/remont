# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.conf import settings
from django.db import models
from django.db.models.signals import m2m_changed
from django.template.defaultfilters import slugify
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from ckeditor.fields import RichTextField
from versatileimagefield.fields import VersatileImageField

ANIMATES = (
    ('Bounce', (
            ('bounceIn', 'bounceIn'),
            ('bounceInDown', 'bounceInDown'),
            ('bounceInLeft', 'bounceInLeft'),
            ('bounceInRight', 'bounceInRight'),
            ('bounceInUp', 'bounceInUp'),
        )
    ),
    ('Fade', (
            ('fadeIn', 'fadeIn'),
            ('fadeInDown', 'fadeInDown'),
            ('fadeInDownBig', 'fadeInDownBig'),
            ('fadeInLeft', 'fadeInLeft'),
            ('fadeInLeftBig', 'fadeInLeftBig'),
            ('fadeInRight', 'fadeInRight'),
            ('fadeInRightBig', 'fadeInRightBig'),
            ('fadeInUp', 'fadeInUp'),
            ('fadeInUpBig', 'fadeInUpBig'),
        )
    ),
    ('Flip', (
            ('flipInX', 'flipInX'),
            ('flipInY', 'flipInY'),
        )
    ),
    ('Lightspeed', (
            ('lightSpeedIn', 'lightSpeedIn'),
        )
    ),
    ('Rotate', (
            ('rotateIn', 'rotateIn'),
            ('rotateInDownLeft', 'rotateInDownLeft'),
            ('rotateInDownRight', 'rotateInDownRight'),
            ('rotateInUpLeft', 'rotateInUpLeft'),
            ('rotateInUpRight', 'rotateInUpRight'),
        )
    ),
    ('Slide', (
            ('slideInUp', 'slideInUp'),
            ('slideInDown', 'slideInDown'),
            ('slideInLeft', 'slideInLeft'),
            ('slideInRight', 'slideInRight'),
        )
    ),
    ('Zoom', (
            ('zoomIn', 'zoomIn'),
            ('zoomInDown', 'zoomInDown'),
            ('zoomInLeft', 'zoomInLeft'),
            ('zoomInRight', 'zoomInRight'),
            ('zoomInUp', 'zoomInUp'),
        )
    ),
    ('Specials', (
            ('jackInTheBox', 'jackInTheBox'),
            ('rollIn', 'rollIn'),
        )
    )
)

class Block(models.Model):
    section = models.OneToOneField('Section', models.CASCADE, related_name="block")
    text = RichTextField(max_length=1000, blank=True, null=True)
    background = VersatileImageField(upload_to='block/', max_length=255, blank=True, null=True)
    button_url = models.CharField(max_length=255, blank=True, null=True)
    button_text = models.CharField(max_length=255, blank=True, null=True)
    animate = models.CharField(max_length=255, choices=ANIMATES, default='None', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'block'



class HomePage(models.Model):
    page = models.OneToOneField('Page', models.CASCADE)

    class Meta:
        managed = True
        db_table = 'home_page'




class Page(models.Model):
    slug = models.SlugField(max_length=2048, blank=True)
    title = models.CharField(max_length=512)
    body = models.TextField(blank=True, null=True)
    view = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField()
    layout = models.BooleanField()
    posmenu = models.SmallIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Page, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'page'
        ordering = ['posmenu']


class SectionImage(models.Model):
    section = models.OneToOneField('Section', models.CASCADE, related_name="image")
    image = VersatileImageField(upload_to='sectionimage/', max_length=255)
    position = models.BooleanField()
    animate = models.CharField(max_length=255, choices=ANIMATES, blank=False, null=True)

    class Meta:
        managed = True
        db_table = 'section_image'


class Section(models.Model):
    page = models.ForeignKey(Page, models.CASCADE, related_name="sections")
    title = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True)
    section_type = models.CharField(max_length=255, choices=(('block', 'block'), ('carusel', 'carusel'), ('table', 'table'), ('filter', 'filter'), ('map', 'map')))
    display_title = models.BooleanField()
    pos = models.IntegerField(blank=True, null=True)
    title_animate = models.CharField(max_length=255, choices=ANIMATES, default='None', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Section, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'section'
        ordering = ['pos']


class FilterCategory(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'filter_category'


class FilterItem(models.Model):
    image = VersatileImageField(upload_to='filteritem/', max_length=255)
    text = models.TextField(max_length=255)
    button_text = models.CharField(max_length=255, blank=True, null=True)
    button_url = models.CharField(max_length=255, blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    categories = models.ManyToManyField("FilterCategory", blank=True, related_name="filter_category")
    section = models.ForeignKey(Section, models.CASCADE, related_name="filter")
    animate = models.CharField(max_length=255, choices=ANIMATES, default='None', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'filter_item'
        ordering = ['position']

        

class CaruselItem(models.Model):
    section = models.ForeignKey(Section, models.CASCADE, related_name="carusel")
    image = VersatileImageField(upload_to='caruselitem/', max_length=255)
    text = RichTextField(max_length=1000, blank=True, null=True)
    button_text = models.CharField(max_length=255, blank=True, null=True)
    button_url = models.CharField(max_length=255, blank=True, null=True)
    text_color = models.CharField(max_length=255, blank=True, null=True)
    animate = models.CharField(max_length=255, choices=ANIMATES, default='None', blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'carusel_item'


class MapItem(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    hint = models.CharField(max_length=255, blank=True, null=True)
    baloon = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    object = models.CharField(max_length=255, blank=True, null=True)
    section = models.ManyToManyField('Section', related_name="map")

    class Meta:
        managed = True
        db_table = 'map_item'

class Table(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    section = models.ForeignKey(Section, models.CASCADE, related_name="table")
    position = models.IntegerField(blank=True, null=True)
    animate = models.CharField(max_length=255, choices=ANIMATES, default='None', blank=True, null=True)

    def clean(self):
        tables = Table.objects.filter(section=self.section).count()
        if tables > 2:
            raise ValidationError("В одной секции может быть максимум 2 таблицы!")

    class Meta:
        managed = True
        db_table = 'table'
        ordering = ['position']



class TableItem(models.Model):
    row = models.IntegerField()
    col = models.IntegerField()
    value = models.CharField(max_length=255, blank=True, null=True)
    table = models.ForeignKey(Table, models.CASCADE, related_name="table_items")

    class Meta:
        managed = True
        db_table = 'table_item'
        unique_together = (("row", "col", 'table'),)

class Feedback(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    text = models.TextField(max_length=1000, blank=True, null=True)
    image = models.ImageField(upload_to='feedback/', max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'feedback'
