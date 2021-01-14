import json

from django.http import HttpResponseRedirect, JsonResponse

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
    # man_collection = ItemType.objects.filter(item__collection__subcategory__category_id=1, is_show_at_index=True)
    # woman_collection = ItemType.objects.filter(item__collection__subcategory__category_id=2, is_show_at_index=True)
    collections = Collection.objects.filter(is_show_at_home=True)
    banner = Banner.objects.all().first()
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
        color["images"] = []

    for type in types:
        stores = ItemAtStore.objects.filter(item_type=type)

        if stores:
            for color in colors:
                if color["color_id"] == type.color.id:
                    size_to_add = {
                         "size_id": type.size.id,
                        "size_name": type.size.name,
                        "heights": []
                    }
                    if not size_to_add in color["sizes"]:
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


    for color in colors:
        images = ItemImage.objects.filter(item=type.item, color_id=color['color_id'])
        for image in images:
            image_to_add={
                "image_id":image.id,
                "image":image.image.url,
            }
            color['images'].append(image_to_add)

    itemInfo = json.dumps(colors)
    # print(colors)
    return render(request, 'pages/item.html', locals())


def subcategory(request,cat_slug,subcat_slug):
    if cat_slug == 'man':
        slider_text ='Мужская медицинская одежда'
    else:
        slider_text = 'Женская медицинская одежда'
    collections = Collection.objects.filter(subcategory__name_slug=subcat_slug)

    return render(request, 'pages/subcategory.html', locals())
def category(request,cat_slug):
    if cat_slug == 'man':
        slider_text ='Мужская медицинская одежда'
    else:
        slider_text = 'Женская медицинская одежда'
    subCats = SubCategory.objects.filter(category__name_slug=cat_slug)
    return render(request, 'pages/category.html', locals())


def new_order(request):
    order_code = create_password()
    if request.user.is_authenticated:
        order = Order.objects.create(client=request.user, order_code=order_code,
                                     payment=request.POST.get('pay'),
                                     delivery=request.POST.get('delivery'),
                                     comment=request.POST.get('comment'),
                                     promo_code=request.user.promo_code
                                     )
        all_cart_items = Cart.objects.filter(client=request.user)
        request.user.promo_code = None
        request.user.save()
    else:
        s_key = request.session.session_key
        guest = Guest.objects.get(session=s_key)
        order = Order.objects.create(guest=guest, order_code=order_code,
                                     payment=request.POST.get('pay'),
                                     delivery=request.POST.get('delivery'),
                                     comment=request.POST.get('comment'),
                                     promo_code=guest.promo_code)
        guest.promo_code = None
        guest.save()
        all_cart_items = Cart.objects.filter(guest=guest)

    for item in all_cart_items:

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

def new_item(request):
    if request.user.is_superuser:
        all_base_items = Item.objects.all()
        all_colors = ItemColor.objects.all()
        all_sizes = ItemSize.objects.all()
        all_heigths = ItemHeight.objects.all()
        return render(request, 'pages/new_item.html', locals())

def create_item(request):

    if request.POST:
        # try:
            #item = ItemType.objects.
        for height in request.POST.getlist('heights'):
            print(height)
            ItemType.objects.create(item_id=request.POST.get('item_id'),
                                    color_id=request.POST.get('color_id'),
                                    size_id=request.POST.get('size_id'),
                                    height_id=height)
    return HttpResponseRedirect('/new_item')


def storage(request):
    if request.user.is_superuser:
        if request.GET.get('sort'):
            all_items = ItemType.objects.all().order_by(f'-{request.GET.get("sort")}')
        else:
            all_items = ItemType.objects.all()
        all_storage = Store.objects.all()
        return render(request, 'pages/storage.html', locals())

def add_item(request):
    if request.user.is_superuser:
        storage = request.GET.get('storage')
        item = request.GET.get('item')
        item = ItemAtStore.objects.get(item_type_id=item,store_id=storage)
        item.item_number+=1
        item.save()
        return HttpResponseRedirect('/storage/')
def del_item(request):
    if request.user.is_superuser:
        storage = request.GET.get('storage')
        item = request.GET.get('item')
        item = ItemAtStore.objects.get(item_type_id=item, store_id=storage)
        if item.item_number > 0:
            item.item_number -= 1
            item.save()
        return HttpResponseRedirect('/storage/')


def search_city(request):
    body = json.loads(request.body)
    return_dict = []
    cities = City.objects.filter(name_lower__contains=body['city'])
    for c in cities:
        return_dict.append(
            {
                "id":c.id,
                "name":c.name,
                "price":c.price
            }
        )
    return JsonResponse(return_dict,safe=False)