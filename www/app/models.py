# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from os import listdir
from os.path import isfile, join
from django.conf import settings
from django.db import models
from django.db.models import Max, Min, F
from django.db.models.signals import m2m_changed
from django.template.defaultfilters import slugify
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from ckeditor.fields import RichTextField
from versatileimagefield.fields import VersatileImageField

def files():
    path = join(settings.BASE_DIR, 'app/templates/app/temp/')
    allfiles = [f for f in listdir(path) if isfile(join(path, f))]
    return tuple(zip(allfiles, allfiles))

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
    section = models.OneToOneField('Section', models.CASCADE, related_name="block", verbose_name="Секция")
    text = RichTextField(max_length=1000, blank=True, null=True, verbose_name="Текст")
    background = VersatileImageField(upload_to='block/', max_length=255, blank=True, null=True, verbose_name="Фон")
    button_url = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ссылка")
    button_text = models.CharField(max_length=255, blank=True, null=True, verbose_name="Текст кнопки")
    animate = models.CharField(max_length=255, choices=ANIMATES, default='None', blank=True, null=True, verbose_name="Анимация")

    def __str__(self):
        return f'Блок секции {self.section}'

    class Meta:
        managed = True
        db_table = 'block'
        verbose_name = 'Блок'
        verbose_name_plural = "Блоки"



class HomePage(models.Model):
    page = models.OneToOneField('Page', models.CASCADE, related_name="homePage")

    def __str__(self):
        return f'Домашняя страница {page.title}'

    class Meta:
        managed = True
        db_table = 'home_page'
        verbose_name = "Домашняя страница"
        verbose_name_plural = "Домашние страницы"




class Page(models.Model):
    slug = models.SlugField(max_length=255, blank=True, verbose_name="ЧПУ")
    title = models.CharField(max_length=255, verbose_name="Название")
    body = models.TextField(blank=True, null=True, verbose_name="Содержимое")
    view = models.CharField(max_length=255, choices=files(), blank=True, null=True, verbose_name="Файл отображения")
    status = models.BooleanField(verbose_name="Отображать")
    layout = models.BooleanField(verbose_name="Использовать шаблон")
    posmenu = models.SmallIntegerField(blank=True, null=True, verbose_name="Позиция в меню")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлена")

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        last = Page.objects.exclude(id=self.id).aggregate(max_posmenu=Max('posmenu')).get('max_posmenu')
        if last:
            if self.posmenu > last + 1:
                self.posmenu = last + 1
        else:
            self.posmenu = 1
        if self.posmenu and self.pk is None:
            if self.posmenu > last:
                self.posmenu = last + 1
            else:
                Page.objects.filter(posmenu__gte=self.posmenu).update(posmenu=F('posmenu') + 1)
        else:
            orig = Page.objects.get(pk=self.pk)
            if orig.posmenu != self.posmenu:
                if orig.posmenu < self.posmenu:
                    Page.objects.filter(posmenu__gte=self.posmenu).filter(posmenu__lte=orig.posmenu).update(posmenu=F('posmenu') - 1)
                if orig.posmenu > self.posmenu:
                    Page.objects.filter(posmenu__gte=self.posmenu).filter(posmenu__lte=orig.posmenu).update(posmenu=F('posmenu') + 1)
        super(Page, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'page'
        ordering = ['posmenu']
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"


class SectionImage(models.Model):
    section = models.OneToOneField('Section', models.CASCADE, related_name="image", verbose_name="Секция")
    image = VersatileImageField(upload_to='sectionimage/', max_length=255, verbose_name="Изображение")
    position = models.BooleanField(verbose_name="Позиция")
    animate = models.CharField(max_length=255, choices=ANIMATES, blank=False, null=True, verbose_name="Анимация")
    
    def __str__(self):
        return f'Изображение секции {self.section}'

    class Meta:
        managed = True
        db_table = 'section_image'
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"


class Section(models.Model):
    page = models.ForeignKey(Page, models.CASCADE, related_name="sections", verbose_name="Страница")
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, blank=True, verbose_name="ЧПУ")
    section_type = models.CharField(max_length=255, choices=(('block', 'Блок'), ('carusel', 'Карусель'), ('table', 'Таблица'), ('filter', 'Фильтр'), ('map', 'Карта')), verbose_name="Тип секции")
    display_title = models.BooleanField(verbose_name="Показывать название")
    pos = models.IntegerField(blank=True, null=True, verbose_name="Позиция")
    title_animate = models.CharField(max_length=255, choices=ANIMATES, default='None', blank=True, null=True, verbose_name="Анимация заголовка")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        rel = ['block', 'table', 'image', 'filter', 'carusel', 'map']
        rel.remove(self.section_type);
        if self.section_type == 'block' or (self.section_type == 'table' and self.table.all().count() < 2):
            rel.remove('image')
        links = [f for f in Section._meta.get_fields()
                #if (f.one_to_many or f.one_to_one)
                if f.auto_created and not f.concrete
        ]
        if self.pk is not None:
            for link in links:
                if link.name in rel:
                    if hasattr(self, link.name):
                        objects = getattr(self, link.name).all().delete()
        last = Section.objects.exclude(id=self.id).aggregate(max_pos=Max('pos')).get('max_pos')
        if last:
            self.pos = last + 1
        else:
            self.pos = 1
        if self.pos and self.pk is None:
            if self.pos > last:
                self.pos = last + 1
            else:
                Section.objects.filter(pos__gte=self.pos).update(pos=F('pos') + 1)
        else:
            orig = Section.objects.get(pk=self.pk)
            if orig.pos != self.pos:
                if orig.pos < self.pos:
                    Section.objects.filter(pos__gte=self.pos).filter(pos__lte=orig.pos).update(pos=F('pos') - 1)
                if orig.pos > self.pos:
                    Section.objects.filter(pos__gte=self.pos).filter(pos__lte=orig.pos).update(pos=F('pos') + 1)
        super(Section, self).save(*args, **kwargs)

    def __str__(self):
        if self.title:
            return f'Секция {self.title} на странице {self.page}'
        else:
            return f'Секция {self.pos} на странице {self.page}'

    class Meta:
        managed = True
        db_table = 'section'
        ordering = ['pos']
        verbose_name = "Секция"
        verbose_name_plural = "Секции"


class FilterCategory(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")

    def __str__(self):
        return f'Категория {self.title}'

    class Meta:
        managed = True
        db_table = 'filter_category'
        verbose_name = "Категория фильтра"
        verbose_name_plural = "Категории фильтра"


class FilterItem(models.Model):
    image = VersatileImageField(upload_to='filteritem/', max_length=255, verbose_name="Изображение")
    text = models.TextField(max_length=255, verbose_name="Текст")
    button_text = models.CharField(max_length=255, blank=True, null=True, verbose_name="Текст кнопки")
    button_url = models.CharField(max_length=255, blank=True, null=True, verbose_name="Url кнопки")
    pos = models.IntegerField(blank=True, null=True, verbose_name="Позиция")
    width = models.IntegerField(blank=True, null=True, verbose_name="Ширина")
    height = models.IntegerField(blank=True, null=True, verbose_name="Высота")
    categories = models.ManyToManyField("FilterCategory", blank=True, related_name="filter_category", verbose_name="Категории")
    section = models.ForeignKey(Section, models.CASCADE, related_name="filter", verbose_name="Секция")
    animate = models.CharField(max_length=255, choices=ANIMATES, default='None', blank=True, null=True, verbose_name="Анимация")
    
    def __str__(self):
        return f'Фильтр {self.section}'

    def save(self, *args, **kwargs):
        if not self.width:
            self.width = 1
        if not self.height:
            self.height = 1
        last = FilterItem.objects.exclude(id=self.id).aggregate(max_pos=Max('pos')).get('max_pos')
        if last:
            self.pos = last + 1
        else:
            self.pos = 1
        if self.pos and self.pk is None:
            if self.pos > last:
                self.pos = last + 1
            else:
                FilterItem.objects.filter(pos__gte=self.pos).update(pos=F('pos') + 1)
        else:
            orig = FilterItem.objects.get(pk=self.pk)
            if orig.pos != self.pos:
                if orig.pos < self.pos:
                    FilterItem.objects.filter(pos__gte=self.pos).filter(pos__lte=orig.pos).update(pos=F('pos') - 1)
                if orig.pos > self.pos:
                    FilterItem.objects.filter(pos__gte=self.pos).filter(pos__lte=orig.pos).update(pos=F('pos') + 1)
        super(FilterItem, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'filter_item'
        ordering = ['pos']
        verbose_name = "Элемент фильтра"
        verbose_name_plural = "Элементы фильтра"

        

class CaruselItem(models.Model):
    section = models.ForeignKey(Section, models.CASCADE, related_name="carusel", verbose_name="Секция")
    image = VersatileImageField(upload_to='caruselitem/', max_length=255, verbose_name="Изображение")
    text = RichTextField(max_length=1000, blank=True, null=True, verbose_name="Текст")
    button_text = models.CharField(max_length=255, blank=True, null=True, verbose_name="Текст кнопки")
    button_url = models.CharField(max_length=255, blank=True, null=True, verbose_name="Url кнопки")
    animate = models.CharField(max_length=255, choices=ANIMATES, default='None', blank=True, null=True, verbose_name="Анимация")
    
    def __str__(self):
        return f'Элемент карусели {self.section}'

    class Meta:
        managed = True
        db_table = 'carusel_item'
        verbose_name = "Элемент карусели"
        verbose_name_plural = "Элементы карусели"


class MapItem(models.Model):
    latitude = models.FloatField(verbose_name="Широта")
    longitude = models.FloatField(verbose_name="Долгота")
    hint = models.CharField(max_length=255, blank=True, null=True, verbose_name="Хинт")
    baloon = models.CharField(max_length=255, blank=True, null=True, verbose_name="Балун")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Адрес")
    object = models.CharField(max_length=255, blank=True, null=True, verbose_name="Объект")
    section = models.ManyToManyField('Section', related_name="map", verbose_name="Секция")

    def __str__(self):
        return f'Элемент карты {self.section}'

    class Meta:
        managed = True
        db_table = 'map_item'
        verbose_name = "Элемент карты"
        verbose_name_plural = "Элементы карты"

class Table(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название")
    section = models.ForeignKey(Section, models.CASCADE, related_name="table", verbose_name="секция")
    pos = models.IntegerField(blank=True, null=True, verbose_name="Позиция")
    animate = models.CharField(max_length=255, choices=ANIMATES, default='None', blank=True, null=True, verbose_name="Анимация")

    def __str__(self):
        if self.title:
            return f'Таблица {self.title}'
        else:
            return f'Таблица {section}'

    def clean(self):
        tables = Table.objects.filter(section=self.section).count()
        if tables > 2:
            raise ValidationError("В одной секции может быть максимум 2 таблицы!")

    def save(self, *args, **kwargs):
        last = Table.objects.exclude(id=self.id).aggregate(max_pos=Max('pos')).get('max_pos')
        if last:
            self.pos = last + 1
        else:
            self.pos = 1
        if self.pos and self.pk is None:
            if self.pos > last:
                self.pos = last + 1
            else:
                Table.objects.filter(pos__gte=self.pos).update(pos=F('pos') + 1)
        else:
            orig = Table.objects.get(pk=self.pk)
            if orig.pos != self.pos:
                if orig.pos < self.pos:
                    Table.objects.filter(pos__gte=self.pos).filter(pos__lte=orig.pos).update(pos=F('pos') - 1)
                if orig.pos > self.pos:
                    Table.objects.filter(pos__gte=self.pos).filter(pos__lte=orig.pos).update(pos=F('pos') + 1)
        super(Table, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'table'
        ordering = ['pos']
        verbose_name = "Таблица"
        verbose_name_plural = "Таблицы"



class TableItem(models.Model):
    row = models.IntegerField(verbose_name="Строка")
    col = models.IntegerField(verbose_name="Столбец")
    value = models.CharField(max_length=255, blank=True, null=True, verbose_name="Значение")
    table = models.ForeignKey(Table, models.CASCADE, related_name="table_items", verbose_name="Таблица")

    def __str__(self):
        return f'Элемент таблицы {self.table}'

    class Meta:
        managed = True
        db_table = 'table_item'
        unique_together = (("row", "col", 'table'),)
        verbose_name = "Элемент таблицы"
        verbose_name_plural = "Элементы таблицы"

class Feedback(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    phone = models.CharField(max_length=255, verbose_name="Телефон")
    text = models.TextField(max_length=1000, blank=True, null=True, verbose_name="Текст")
    image = models.ImageField(upload_to='feedback/', max_length=255, blank=True, null=True, verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    def __str__(self):
        return f'Заявка {self.pk}'

    class Meta:
        managed = True
        db_table = 'feedback'
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
