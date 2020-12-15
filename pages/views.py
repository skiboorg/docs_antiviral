import json

from django.shortcuts import render
from shop.models import *


def index(request):
    man_collection = ItemType.objects.filter(item__collection__subcategory__category_id=1, is_show_at_index=True)
    woman_collection = ItemType.objects.filter(item__collection__subcategory__category_id=2, is_show_at_index=True)
    return render(request, 'pages/index.html', locals())


def about(request):

    return render(request, 'pages/about.html', locals())


def delivery(request):

    return render(request, 'pages/delivery.html', locals())


def contacts(request):

    return render(request, 'pages/contact.html', locals())


def partner(request):

    return render(request, 'pages/parnter.html', locals())


def item(request,cat_slug,subcat_slug,item_slug):
    item = Item.objects.get(name_slug=item_slug)
    info = []
    colors=[]
    sizes=[]
    heights=[]
    types = ItemType.objects.filter(item=item)
    for type in types:
        stores = ItemAtStore.objects.filter(item_type=type)
        if stores:
            color_for_add = {
                "color_id": type.color.id,
                "color_hex": type.color.bg_color,
            }
            if not color_for_add in colors:
                colors.append(color_for_add)

    for color in colors:
        color["sizes"] = []
        color["heights"] = []
    for type in types:
        stores = ItemAtStore.objects.filter(item_type=type)
        print(stores)
        if stores:
            for color in colors:
                if color["color_id"] == type.color.id:
                    size_to_add = {
                         "size_id": type.size.id,
                        "size_name": type.size.name,

                    }
                    color["sizes"].append(size_to_add)
                    height_to_add = {
                        "height_id": type.height.id,
                        "height_name": type.height.name,
                        "type_slug": type.name_slug

                    }
                    color["heights"].append(height_to_add)
    print(json.dumps(colors))
    itemInfo = json.dumps(colors)
    return render(request, 'pages/item.html', locals())


def subcategory(request,cat_slug,subcat_slug):

    collections = Collection.objects.filter(subcategory__name_slug=subcat_slug)
    print(collections)
    return render(request, 'pages/subcategory.html', locals())
def category(request,cat_slug):
    subCats = SubCategory.objects.filter(category__name_slug=cat_slug)
    return render(request, 'pages/category.html', locals())
