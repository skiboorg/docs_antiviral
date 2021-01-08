from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import post_save
from pytils.translit import slugify
from random import choices
import string
from colorfield.fields import ColorField
from django.utils.safestring import mark_safe

class Category(models.Model):
    name = models.CharField('Название категории', max_length=255, blank=True, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField('Изображение категории', upload_to='images/catalog/categories/', blank=True)
    page_h1 = models.CharField('Тег H1', max_length=255, blank=True, null=True)
    page_title = models.CharField('Title страницы', max_length=255, blank=True, null=True)
    description = RichTextUploadingField('Описание категории', blank=True, null=True)
    is_active = models.BooleanField('Отображать ?', default=True, db_index=True)
    order_num = models.IntegerField(default=100)
    views = models.IntegerField(default=0,editable=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class SubCategory(models.Model):
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Категория',
                                 related_name='subcategory')
    name = models.CharField('Название подкатегории', max_length=255, blank=True, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True,editable=False)
    image = models.ImageField('Изображение категории', upload_to='images/catalog/categories/', blank=True)
    page_h1 = models.CharField('Тег H1', max_length=255, blank=True, null=True)
    page_title = models.CharField('Title страницы', max_length=255, blank=True, null=True)
    description = RichTextUploadingField('Описание категории', blank=True, null=True)
    is_active = models.BooleanField('Отображать ?', default=True, db_index=True)
    is_in_index_catalog = models.BooleanField('Показывать на главной ?', default=False, db_index=True)
    order_num = models.IntegerField(default=100)
    views = models.IntegerField(default=0,editable=False)

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        if not self.name_slug:
            testSlug = SubCategory.objects.filter(name_slug=slug)
            slugRandom = ''
            if testSlug:
                slugRandom = '-' + ''.join(choices(string.ascii_lowercase + string.digits, k=2))
            self.name_slug = slug + slugRandom
        super(SubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

class Collection(models.Model):
    subcategory = models.ForeignKey(SubCategory, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Относится к')
    name = models.CharField('Название', max_length=255, blank=True, null=True)
    description = models.CharField('Описание', max_length=255, blank=True, null=True)
    is_show_at_home = models.BooleanField('Отображать на главной', default=False)

    def __str__(self):
        return f'Коллекция {self.name} подкатегории {self.subcategory.name}'

    class Meta:
        verbose_name = "Коллекция"
        verbose_name_plural = "Коллекции"

class ItemColor(models.Model):
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    name = models.CharField('Название', max_length=255, blank=True, null=True)
    bg_color = ColorField('Цвет', default='#000000')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(ItemColor, self).save(*args, **kwargs)

class ItemSize(models.Model):
    name = models.CharField('Размер', max_length=255, blank=True, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(ItemSize, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"

class ItemHeight(models.Model):
    name = models.CharField('Рост', max_length=255, blank=True, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(ItemHeight, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Рост"
        verbose_name_plural = "Рост"

class Item(models.Model):
    collection = models.ForeignKey(Collection, verbose_name='Коллекция',
                                   on_delete=models.SET_NULL, blank=True, null=True, db_index=True,
                                   related_name='items')

    name = models.CharField('Название товара', max_length=255, blank=True, null=True)
    name_lower = models.CharField(max_length=255, blank=True, null=True,default='',editable=False)
    name_slug = models.CharField(max_length=255, blank=True, null=True,db_index=True,editable=False)
    price = models.IntegerField('Цена', blank=True, default=0, db_index=True)
    old_price = models.IntegerField('Цена без скидки', blank=True, default=0, db_index=True)
    article = models.CharField('Артикул', max_length=50, blank=True, null=True)
    discount = models.IntegerField('Скидка', default=0)
    short_description = models.TextField('Короткое описание', blank=True, null=True)
    page_title = models.CharField('Title страницы', max_length=255, blank=True, null=True)
    page_description = models.TextField('Description страницы', blank=True, null=True)

    description = RichTextUploadingField('Тект для вкладки Детали', blank=True, null=True)
    carry = RichTextUploadingField('Тект для вкладки Состав и уход', blank=True, null=True)
    delivery = RichTextUploadingField('Тект для вкладки Срок доставки', blank=True, null=True)


    is_active = models.BooleanField('Отображать товар ?', default=True, db_index=True)
    is_present = models.BooleanField('Товар в наличии ?', default=True, db_index=True)
    is_new = models.BooleanField('Товар новинка ?', default=False, db_index=True)
    buys = models.IntegerField(default=0,editable=False)
    views = models.IntegerField(default=0,editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def image_tag(self):
        # used in the admin site model as a "thumbnail"
        if self.images.first():
            return mark_safe('<img src="{}" width="100" height="100" />'.format(self.images.first().image.url))
        else:
            return mark_safe('<span>НЕТ МИНИАТЮРЫ</span>')

    image_tag.short_description = 'Основная картинка'

    def save(self, *args, **kwargs):
        if self.old_price == 0:
            self.old_price = self.price
        if self.discount > 0:
            self.old_price = self.price
            self.price = self.price - (self.price * self.discount / 100)
        else:
            self.price = self.old_price


        slug = slugify(self.name)
        if not self.name_slug:
            testSlug = Item.objects.filter(name_slug=slug)
            slugRandom = ''
            if testSlug:
                slugRandom = '-' + ''.join(choices(string.ascii_lowercase + string.digits, k=2))
            self.name_slug = slug + slugRandom
        self.name_lower = self.name.lower()
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Базовый товар"
        verbose_name_plural = "Базовые товары"


class ItemType(models.Model):


    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True,editable=False)
    item = models.ForeignKey(Item, verbose_name='Базовый товар',
                                    on_delete=models.CASCADE, blank=True,null=True,db_index=True)
    color = models.ForeignKey(ItemColor, verbose_name='Цвет',
                             on_delete=models.CASCADE, blank=True, null=True, db_index=True,related_name='colors')
    size = models.ForeignKey(ItemSize, verbose_name='Размер',
                             on_delete=models.CASCADE, blank=True, null=True, db_index=True,related_name='sizes')
    height = models.ForeignKey(ItemHeight, verbose_name='Рост',
                             on_delete=models.CASCADE, blank=True, null=True, db_index=True,related_name='heights')
    is_show_at_index = models.BooleanField(default=False)

    def __str__(self):
        return f'Вид товара : {self.item.name} | {self.color.name} | {self.size.name} | {self.height.name}'

    class Meta:
        verbose_name = "Вид товара"
        verbose_name_plural = "Виды товаров"

    def save(self, *args, **kwargs):
        self.name_slug = f'{self.item.name_slug}-{self.color.name_slug}-{self.size.name_slug}-{self.height.name_slug}'
        super(ItemType, self).save(*args, **kwargs)

    def color_tag(self):
        return self.color.name
    color_tag.short_description = 'Цвет'

    def article_tag(self):
        return self.item.article
    article_tag.short_description = 'Артикул'

    def name_tag(self):
        return self.item.name
    name_tag.short_description = 'Название'

    def size_tag(self):
        return self.size.name
    name_tag.short_description = 'Размер'



class ItemImage(models.Model):
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.CASCADE, verbose_name='К товару', related_name='images')
    image = models.ImageField('Изображение товара', upload_to='images/catalog/items/', blank=True)
    # color = models.ForeignKey(ItemColor, verbose_name='Цвет',
    #                           on_delete=models.CASCADE, blank=True, null=True, db_index=True)
    color = models.ForeignKey(ItemColor, on_delete=models.SET_NULL, verbose_name='Цвет', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s Изображение для товара : %s ' % (self.id, self.item.name)

    class Meta:
        verbose_name = "Изображение для товара"
        verbose_name_plural = "Изображения для товара"

    def image_tag(self):
        # used in the admin site model as a "thumbnail"
        if self.image:
            return mark_safe('<img src="{}" width="150" height="150" />'.format(self.image.url))
        else:
            return mark_safe('<span>НЕТ МИНИАТЮРЫ</span>')

    image_tag.short_description = 'Картинка'


class Store(models.Model):
    name = models.CharField('Название склада', max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"

class ItemAtStore(models.Model):
    store = models.ForeignKey(Store, blank=True, null=True, on_delete=models.CASCADE, verbose_name='На складе')
    item_type = models.ForeignKey(ItemType, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Тип товара')
    item_number = models.IntegerField('Остаток',default=0)

    def __str__(self):
        return f'Товар {self.item_type.item.name} | {self.item_type.size} | {self.item_type.height} | {self.item_type.color} на складе {self.store.name} остаток {self.item_number}'

    class Meta:
        verbose_name = "Товар на складе"
        verbose_name_plural = "Товары на складах"


class PromoCode(models.Model):
    code = models.CharField('ПромоКод', max_length=255, blank=False, null=True)
    discount = models.IntegerField('Скидка % по коду',default=0)
    summ = models.IntegerField('Скидка в рублях по коду',default=0)

    def __str__(self):
        return f'Промо код {self.code} | Скидка {self.discount}% | Скидка {self.summ}руб'
    class Meta:
        verbose_name = "Промо код"
        verbose_name_plural = "Промо коды"

def item_type_post_save(sender, instance, created, **kwargs):
    if created:
        all_stores = Store.objects.all()
        for store in all_stores:
            ItemAtStore.objects.create(item_type=instance,store=store)

post_save.connect(item_type_post_save, sender=ItemType)
