from django.contrib import admin
from .models import *

class ImagesInline (admin.TabularInline):
    model = ItemImage
    readonly_fields = ('image_tag', )
    extra = 0

class ItemAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'name', 'article', 'price', ]
    inlines = [ImagesInline]
    class Meta:
        model = Item

class ItemTypeAdmin(admin.ModelAdmin):

    list_filter = ("item",)
    class Meta:
        model = ItemType

admin.site.register(ItemImage)
admin.site.register(Store)
admin.site.register(PromoCode)
admin.site.register(ItemAtStore)
admin.site.register(Item,ItemAdmin)
admin.site.register(Collection)
admin.site.register(ItemSize)
admin.site.register(ItemHeight)
admin.site.register(ItemColor)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(ItemType,ItemTypeAdmin)
