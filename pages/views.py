import json

from django.http import HttpResponseRedirect

from order.models import *
from django.shortcuts import render
from shop.models import *
from cart.models import *
def create_password():
    from random import choices
    import string
    password = ''.join(choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8))
    return password


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
                "color_name": type.color.name
            }
            if not color_for_add in colors:
                colors.append(color_for_add)

    for color in colors:
        color["sizes"] = []

    for type in types:
        stores = ItemAtStore.objects.filter(item_type=type)
        print(stores)
        if stores:
            for color in colors:
                if color["color_id"] == type.color.id:
                    size_to_add = {
                         "size_id": type.size.id,
                        "size_name": type.size.name,
                        "heights":[]

                    }
                    color["sizes"].append(size_to_add)

    for type in types:
        for color in colors:
            for size in color['sizes']:
                if color['color_id'] == type.color.id and size['size_id'] == type.size.id:
                    height_to_add = {
                        "height_id": type.height.id,
                        "height_name": type.height.name,

                    }
                    size['heights'].append(height_to_add)

    print(colors)
    itemInfo = json.dumps(colors)
    return render(request, 'pages/item.html', locals())


def subcategory(request,cat_slug,subcat_slug):

    collections = Collection.objects.filter(subcategory__name_slug=subcat_slug)
    print(collections)
    return render(request, 'pages/subcategory.html', locals())
def category(request,cat_slug):
    subCats = SubCategory.objects.filter(category__name_slug=cat_slug)
    return render(request, 'pages/category.html', locals())


def new_order(request):
    order_code = create_password()

    print(request.POST)
    if request.user.is_authenticated:
        order = Order.objects.create(client=request.user, order_code=order_code,
                                     payment=request.POST.get('pay'),
                                     delivery=request.POST.get('delivery'),
                                     comment=request.POST.get('comment'))
        all_cart_items = Cart.objects.filter(client=request.user)
    else:
        s_key = request.session.session_key
        guest = Guest.objects.get(session=s_key)
        order = Order.objects.create(guest=guest, order_code=order_code,
                                     payment=request.POST.get('pay'),
                                     delivery=request.POST.get('delivery'),
                                     comment=request.POST.get('comment'))

        all_cart_items = Cart.objects.filter(guest=guest)

    for item in all_cart_items:
        print(item)
        ItemsInOrder.objects.create(order=order, item=item.item, number=item.number,
                                    current_price=item.current_price)


    all_cart_items.delete()
    return HttpResponseRedirect('/order/{}'.format(order.order_code))

def order(request, order_code):
    try:
        order = Order.objects.get(order_code=order_code)
    except:
        order=None

    if order:
        return render(request, 'pages/order_complete.html', locals())
    else:
        return HttpResponseRedirect('/')
