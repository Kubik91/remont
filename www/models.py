# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Blocks(models.Model):
    section = models.ForeignKey('Sections', models.DO_NOTHING)
    text = models.CharField(max_length=255, blank=True, null=True)
    background = models.CharField(max_length=255, blank=True, null=True)
    button_url = models.CharField(max_length=255, blank=True, null=True)
    button_text = models.CharField(max_length=255, blank=True, null=True)
    animate = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'blocks'


class Carusel(models.Model):
    item = models.ForeignKey('CaruselItems', models.DO_NOTHING, primary_key=True)
    section = models.ForeignKey('Sections', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'carusel'
        unique_together = (('item', 'section'),)


class CaruselItems(models.Model):
    image = models.CharField(max_length=255)
    context = models.CharField(max_length=1000, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    button_text = models.CharField(max_length=255, blank=True, null=True)
    button_url = models.CharField(max_length=255, blank=True, null=True)
    text_color = models.CharField(max_length=255, blank=True, null=True)
    animate = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'carusel_items'


class FilterCategory(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'filter_category'


class FilterItems(models.Model):
    filter = models.ForeignKey('Filters', models.DO_NOTHING)
    image = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    button_text = models.CharField(max_length=255, blank=True, null=True)
    button_url = models.CharField(max_length=255, blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'filter_items'


class Filters(models.Model):
    section = models.ForeignKey('Sections', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'filters'


class FiltersCategories(models.Model):
    category = models.ForeignKey(FilterCategory, models.DO_NOTHING, primary_key=True)
    item = models.ForeignKey(FilterItems, models.DO_NOTHING)
    filter_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'filters_categories'
        unique_together = (('category', 'item'),)


class HomePage(models.Model):
    page = models.ForeignKey('Pages', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'home_page'


class Maps(models.Model):
    section = models.ForeignKey('Sections', models.DO_NOTHING)
    latitude = models.IntegerField()
    longitude = models.IntegerField()
    hint = models.CharField(max_length=255, blank=True, null=True)
    baloon = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'maps'


class Pages(models.Model):
    url = models.CharField(max_length=2048)
    title = models.CharField(max_length=512)
    body = models.TextField(blank=True, null=True)
    view = models.CharField(max_length=255, blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=True)
    layout = models.IntegerField(blank=True, null=True)
    posmenu = models.SmallIntegerField(blank=True, null=True)
    created_at = models.IntegerField(blank=True, null=True)
    updated_at = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pages'


class SectionImage(models.Model):
    section = models.ForeignKey('Sections', models.DO_NOTHING)
    image = models.CharField(max_length=255)
    position = models.IntegerField(blank=True, null=True)
    animate = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'section_image'


class Sections(models.Model):
    page = models.ForeignKey(Pages, models.DO_NOTHING)
    title = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255)
    display_title = models.IntegerField(blank=True, null=True)
    pos = models.IntegerField(blank=True, null=True)
    title_animate = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sections'


class Table(models.Model):
    table = models.ForeignKey('Tables', models.DO_NOTHING, primary_key=True)
    row = models.IntegerField()
    col = models.IntegerField()
    value = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'table'
        unique_together = (('table', 'row', 'col'),)


class Tables(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    section = models.ForeignKey(Sections, models.DO_NOTHING)
    pos = models.IntegerField(blank=True, null=True)
    animate = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tables'
